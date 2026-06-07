import { FileText, AlertCircle, Star, CheckCircle, RefreshCw, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useDashboardStats } from '@/hooks/useDashboardStats';

const INFRA_STATUS = [
  { label: 'Vite + React + TypeScript', ok: true },
  { label: 'TailwindCSS + shadcn/ui', ok: true },
  { label: 'React Router', ok: true },
  { label: 'Axios + JWT interceptors', ok: true },
  { label: 'Zustand stores', ok: true },
];

export function DashboardPage() {
  const { stats, loading, error, refresh } = useDashboardStats();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-sm text-muted-foreground">Estado general del sistema</p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={refresh}
          disabled={loading}
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Actualizar
        </Button>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <p className="text-sm text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total documentos</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{loading ? '—' : stats?.documents.total ?? 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.documents.healthy ?? 0} healthy, {stats?.documents.needsImprovement ?? 0} mejorar
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Calificación promedio</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '—' : stats?.documents.avgRating ?? 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.documents.noRating ?? 0} sin calificar
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Gaps pendientes</CardTitle>
            <AlertCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{loading ? '—' : stats?.gaps.pending ?? 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.gaps.byPriority.critical ?? 0} críticos, {stats?.gaps.byPriority.high ?? 0} alta
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Propuestas pendientes</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{loading ? '—' : stats?.proposals.pending ?? 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.proposals.total ?? 0} total, {stats?.proposals.byStatus.implemented ?? 0} aplicadas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Progreso</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '—' : `${stats?.progress.gapsResolvedPercentage ?? 0}%`}
            </div>
            <p className="text-xs text-muted-foreground">
              Gaps resueltos • {stats?.progress.documentsHealthyPercentage ?? 0}% docs healthy
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Estado de infraestructura</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {INFRA_STATUS.map(({ label, ok }) => (
              <li key={label} className="flex items-center gap-2 text-sm">
                <CheckCircle className="h-4 w-4 shrink-0 text-emerald-500" />
                <span>{label}</span>
                {ok && <Badge variant="success" className="ml-auto">OK</Badge>}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
