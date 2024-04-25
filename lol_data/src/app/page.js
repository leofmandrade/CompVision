import Image from "next/image";
import styles from "./page.module.css";


export default function Home() {
  // const photo = require('./narutoBackground3.jpg'); // Importando a imagem localmente

  return (
    <main className={styles.main}>
      <div className={styles.center}>
        <a href="/home">
          <Image
            className={styles.logo}
            src="/next.svg"
            alt="Next.js Logo"
            width={180}
            height={37}
            priority
          />
        </a>

      </div>
    </main>
  );
}

