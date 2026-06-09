import { useEffect } from 'react';
import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { AppLayout } from '@/components/layout/AppLayout';
import { DocumentExplorerLayout } from '@/components/layout/DocumentExplorerLayout';
import { LoginPage } from '@/pages/LoginPage';
import { HomePage } from '@/pages/HomePage';
import { OrganizationPage } from '@/pages/OrganizationPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { DocumentsPage } from '@/pages/DocumentsPage';
import { DocumentDetailPage } from '@/pages/DocumentDetailPage';
import { GapsPage } from '@/pages/GapsPage';
import { GapDetailPage } from '@/pages/GapDetailPage';
import { ProposalsPage } from '@/pages/ProposalsPage';
import { ProposalDetailPage } from '@/pages/ProposalDetailPage';
import { NotFoundPage } from '@/pages/NotFoundPage';

function RequireAuth() {
  const { user, loading } = useAuthStore();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
}

function App() {
  const { fetchMe } = useAuthStore();

  useEffect(() => {
    fetchMe();
  }, [fetchMe]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<RequireAuth />}>
          <Route element={<AppLayout />}>
            {/* Home - List of organizations and projects */}
            <Route index element={<HomePage />} />

            {/* Organization page - shows projects within the organization */}
            <Route path=":orgSlug" element={<OrganizationPage />} />

            {/* Project-scoped routes following GitHub-style URL structure */}
            <Route path=":orgSlug/:projectSlug">
              {/* Project Dashboard - overview/stats */}
              <Route index element={<DashboardPage />} />
              {/* Documents explorer */}
              <Route path="documents" element={<DocumentExplorerLayout />}>
                <Route index element={<DocumentsPage />} />
                <Route path=":slug" element={<DocumentDetailPage />} />
              </Route>
              {/* Gaps */}
              <Route path="gaps" element={<GapsPage />} />
              <Route path="gaps/:slug" element={<GapDetailPage />} />
              {/* Proposals */}
              <Route path="proposals" element={<ProposalsPage />} />
              <Route path="proposals/:id" element={<ProposalDetailPage />} />
            </Route>

            {/* Legacy routes - redirect to project-scoped or keep for compatibility */}
            <Route path="documents" element={<Navigate to="/" replace />} />
            <Route path="gaps" element={<Navigate to="/" replace />} />
            <Route path="proposals" element={<Navigate to="/" replace />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
