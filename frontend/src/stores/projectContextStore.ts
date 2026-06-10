import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import type { Organization, Project } from '@/types/organization';

interface ProjectContextState {
  // Current selection
  currentOrganization: Organization | null;
  currentProject: Project | null;

  // Setters
  setCurrentOrganization: (org: Organization | null) => void;
  setCurrentProject: (project: Project | null) => void;
  setProjectContext: (org: Organization | null, project: Project | null) => void;

  // Clear context
  clearContext: () => void;

  // Computed
  hasContext: () => boolean;
  getContextPath: () => string | null;
}

export const useProjectContextStore = create<ProjectContextState>()(
  persist(
    (set, get) => ({
      currentOrganization: null,
      currentProject: null,

      setCurrentOrganization: (org) => {
        set({ currentOrganization: org });
      },

      setCurrentProject: (project) => {
        set({ currentProject: project });
      },

      setProjectContext: (org, project) => {
        set({
          currentOrganization: org,
          currentProject: project,
        });
      },

      clearContext: () => {
        set({
          currentOrganization: null,
          currentProject: null,
        });
      },

      hasContext: () => {
        const { currentOrganization, currentProject } = get();
        return currentOrganization !== null && currentProject !== null;
      },

      getContextPath: () => {
        const { currentOrganization, currentProject } = get();
        if (!currentOrganization || !currentProject) {
          return null;
        }
        return `/${currentOrganization.slug}/${currentProject.slug}`;
      },
    }),
    {
      name: 'alejandria-project-context',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// Hook to get current project context from URL params
// This synchronizes URL with the store
export function useProjectContextFromParams(orgSlug?: string, projectSlug?: string) {
  const { currentOrganization, currentProject } = useProjectContextStore();

  // If URL params are provided and different from current context, update it
  if (orgSlug && projectSlug) {
    // Check if we need to update (either org or project changed)
    const orgChanged = currentOrganization?.slug !== orgSlug;
    const projectChanged = currentProject?.slug !== projectSlug;

    if (orgChanged || projectChanged) {
      // We need to fetch the org and project details
      // This will be handled by the ProjectSelector component or a layout effect
    }
  }

  return {
    orgSlug,
    projectSlug,
    hasContext: !!orgSlug && !!projectSlug,
  };
}
