/// <reference types="vite/client" />

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_URL_MOVIES: string;
  readonly VITE_URL_HISTORY: string;
  readonly VITE_URL_PROXY: string;
  readonly VITE_CLICKS_COUNT: number;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
