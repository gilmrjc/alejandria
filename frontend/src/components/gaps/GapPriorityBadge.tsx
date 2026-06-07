import { Badge } from '@/components/ui/badge';
import type { GapPriority } from '@/types/gap';

interface GapPriorityBadgeProps {
  priority: GapPriority;
}

const priorityConfig: Record<GapPriority, { label: string; variant: 'default' | 'destructive' | 'success' }> = {
  critical: { label: 'Crítico', variant: 'destructive' },
  high: { label: 'Alto', variant: 'destructive' },
  medium: { label: 'Medio', variant: 'default' },
  low: { label: 'Bajo', variant: 'default' },
};

export function GapPriorityBadge({ priority }: GapPriorityBadgeProps) {
  const config = priorityConfig[priority];
  return <Badge variant={config.variant}>{config.label}</Badge>;
}
