import { NavLink, Outlet, useNavigate, useParams } from 'react-router-dom';
import { LayoutDashboard, LogOut, BookOpen, ChevronRight, FileText, AlertCircle, Lightbulb } from 'lucide-react';
import { cn } from '@/utils';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';
import { useBreadcrumbs } from '@/hooks/useBreadcrumbs';
import { ProjectSelector } from './ProjectSelector';

export function AppLayout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const { orgSlug, projectSlug } = useParams<{ orgSlug?: string; projectSlug?: string }>();
  const breadcrumbs = useBreadcrumbs();

  // Build dynamic nav items based on current project context
  const hasProjectContext = !!orgSlug && !!projectSlug;
  const projectPath = hasProjectContext ? `/${orgSlug}/${projectSlug}` : '';

  const navItems = [
    ...(hasProjectContext
      ? [
          // When in project context, Dashboard links to project dashboard
          { to: projectPath, label: 'Dashboard', icon: LayoutDashboard, end: true },
          { to: `${projectPath}/documents`, label: 'Documentos', icon: FileText, end: false },
          { to: `${projectPath}/gaps`, label: 'Gaps', icon: AlertCircle, end: false },
          { to: `${projectPath}/proposals`, label: 'Propuestas', icon: Lightbulb, end: false },
        ]
      : [
          // When not in project context, Dashboard links to home
          { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
        ]),
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleBreadcrumbClick = (path: string) => {
    navigate(path);
  };

  return (
    <div className="flex h-screen flex-col bg-background">
      <header className="border-b bg-background px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-primary" />
              <span className="font-semibold">Alejandria</span>
            </div>
            {/* Project Selector */}
            <ProjectSelector />
          </div>

          <nav className="flex items-center gap-1">
            {navItems.map(({ to, label, icon: Icon, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors',
                    isActive
                      ? 'bg-accent text-accent-foreground font-medium'
                      : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium">{user?.username}</p>
              <p className="text-xs text-muted-foreground">{user?.email}</p>
            </div>
            <Button variant="ghost" size="sm" onClick={handleLogout} aria-label="Cerrar sesión">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <main className="flex-1 overflow-y-auto p-6">
          {breadcrumbs.length > 1 && (
            <div className="mb-4">
              <nav className="flex items-center gap-2 text-sm text-muted-foreground">
                {breadcrumbs.map((crumb, index) => (
                  <div key={crumb.path} className="flex items-center gap-2">
                    {index > 0 && <ChevronRight className="h-4 w-4" />}
                    <button
                      onClick={() => handleBreadcrumbClick(crumb.path)}
                      disabled={index === breadcrumbs.length - 1}
                      className={cn(
                        'hover:text-foreground transition-colors',
                        index === breadcrumbs.length - 1
                          ? 'text-foreground font-medium cursor-default'
                          : 'cursor-pointer'
                      )}
                    >
                      {crumb.label}
                    </button>
                  </div>
                ))}
              </nav>
            </div>
          )}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
