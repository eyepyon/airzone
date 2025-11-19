// Temporary type declarations for external modules

declare module 'js-cookie' {
  interface CookiesStatic {
    get(name: string): string | undefined;
    set(name: string, value: string, options?: any): string | undefined;
    remove(name: string, options?: any): void;
  }

  const Cookies: CookiesStatic;
  export default Cookies;
}

declare module 'qrcode' {
  export function toCanvas(
    canvas: HTMLCanvasElement,
    text: string,
    options?: any
  ): Promise<void>;
  
  export function toDataURL(text: string, options?: any): Promise<string>;
}
