import Image from "next/image";
import styles from "./page.module.css";
import getUrl from "./geturl/page.js";

// PAGINA PRINCIPAL SEMPRE DIRECIONA PARA A PAGINA DE GETURL
export default function HomePage() {
  // ir direto para a página de getUrl
  return <getUrl />;
}
