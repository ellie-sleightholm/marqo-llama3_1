import "@/styles/globals.css";
import "@/components/ChatWindow.css";
import "@/components/DocumentAdd.css";
import "@/components/BouncingDots.css";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
