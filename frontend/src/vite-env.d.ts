/// <reference types="vite/client" />

/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_URL_MOVIES: string;
    readonly VITE_URL_HISTORY: string;    
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  