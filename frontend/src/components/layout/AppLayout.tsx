import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { LayoutDashboard, LogOut, BookOpen, ChevronRight, FileText, AlertCircle, Lightbulb } from 'lucide-react';
import { cn } from '@/utils';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';
import { useBreadcrumbs } from '@/hooks/useBreadcrumbs';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/documents', label: 'Documentos', icon: FileText, end: false },
  { to: '/gaps', label: 'Gaps', icon: AlertCircle, end: false },
  { to: '/proposals', label: 'Propuestas', icon: Lightbulb, end: false },
];

export function AppLayout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const breadcrumbs = useBreadcrumbs();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleBreadcrumbClick = (path: string) => {
    navigate(path);
  };

  return (
    <div className="flex h-screen bg-background">
      <aside className="flex w-56 flex-col border-r bg-sidebar">
        <div className="flex h-14 items-center gap-2 border-b px-4">
          <BookOpen className="h-5 w-5 text-sidebar-primary" />
          <span className="font-semibold text-sidebar-foreground">Alejandria</span>
        </div>

        <nav className="flex-1 space-y-1 p-2">
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
                  isActive
                    ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium'
                    : 'text-sidebar-foreground hover:bg-sidebar-accent/50'
                )
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t p-3">
          <div className="mb-2 px-3 py-1">
            <p className="truncate text-xs font-medium text-sidebar-foreground">{user?.username}</p>
            <p className="truncate text-xs text-muted-foreground">{user?.email}</p>
          </div>
          <Button variant="ghost" size="sm" className="w-full justify-start gap-2" onClick={handleLogout}>
            <LogOut className="h-4 w-4" />
            Cerrar sesión
          </Button>
        </div>
      </aside>

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="border-b bg-background px-6 py-3">
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
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
