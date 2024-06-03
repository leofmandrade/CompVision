// Importa todos os arquivos de uma pasta
const importAll = (r) => {
    let images = {};
    r.keys().map((item, index) => {
      images[item.replace('./', '')] = r(item);
    });
    return images;
  };
  
  // Importa todos os arquivos da pasta championIcons
  const championIcons = importAll(require.context('../../championIcons', false, /\.(png|jpe?g|svg)$/));
  
  export default championIcons;
  