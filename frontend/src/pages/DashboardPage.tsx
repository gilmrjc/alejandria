import { FileText, AlertCircle, Star, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const MOCK_STATS = [
  { label: 'Total documentos', value: '—', icon: FileText, note: 'Conectar en EPC-0032' },
  { label: 'Calificación promedio', value: '—', icon: Star, note: 'Conectar en EPC-0032' },
  { label: 'Gaps pendientes', value: '—', icon: AlertCircle, note: 'Conectar en EPC-0033' },
];

const INFRA_STATUS = [
  { label: 'Vite + React + TypeScript', ok: true },
  { label: 'TailwindCSS + shadcn/ui', ok: true },
  { label: 'React Router', ok: true },
  { label: 'Axios + JWT interceptors', ok: true },
  { label: 'Zustand stores', ok: true },
];

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-sm text-muted-foreground">Estado general del sistema</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        {MOCK_STATS.map(({ label, value, icon: Icon, note }) => (
          <Card key={label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{label}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{value}</div>
              <p className="text-xs text-muted-foreground">{note}</p>
            </CardContent>
          </Card>
        ))}
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
