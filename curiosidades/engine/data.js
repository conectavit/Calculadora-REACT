// Conteúdo dos 10 vídeos de curiosidade.
// Marcação: *palavra* = destaque colorido no texto.
// Tipos de cena: hook | fact | stat | timeline | compare | cta
// art: "hero" (ilustração SVG própria do vídeo), "hero:variante" ou um emoji.

const VIDEOS = [
  {
    id: 1,
    slug: "01-ilha-das-cobras",
    titulo: "A ilha brasileira onde é proibido pisar",
    tema: { a: "#0b2b1c", b: "#051510", acc: "#c8f04a", acc2: "#ff5d3a" },
    hero: "snake",
    cenas: [
      { t: "hook", text: "Existe uma ilha no *Brasil* onde é *proibido* desembarcar", art: "hero:island" },
      { t: "fact", text: "Ilha da *Queimada Grande*", sub: "No litoral sul de São Paulo, coberta de Mata Atlântica", art: "📍" },
      { t: "stat", big: "2 a 4 mil", text: "jararacas-ilhoas", sub: "vivem numa ilha de apenas 43 hectares", art: "hero" },
      { t: "fact", text: "Essa cobra só existe *ali*", sub: "Em nenhum outro lugar do planeta", art: "🌎" },
      { t: "fact", text: "Sem roedores na ilha, ela aprendeu a caçar *aves migratórias*", sub: "que param ali para descansar", art: "🐦" },
      { t: "fact", text: "O veneno age *rápido* para a presa não fugir voando", sub: "e é estudado pelo Instituto Butantan", art: "🧪" },
      { t: "fact", text: "Só pesquisadores com *autorização* podem entrar", sub: "A espécie está criticamente ameaçada de extinção", art: "⚠️" },
      { t: "cta", text: "Você teria *coragem* de visitar?", sub: "Comenta aí 👇 e segue pra parte 2" },
    ],
    narracao:
      "Existe uma ilha no Brasil onde é proibido desembarcar. É a Ilha da Queimada Grande, no litoral sul de São Paulo. Nos seus 43 hectares vivem de 2 a 4 mil jararacas-ilhoas, uma cobra que não existe em nenhum outro lugar do planeta. Como a ilha não tem roedores, ela aprendeu a caçar aves migratórias que param ali para descansar. Por isso o veneno age rápido: a presa não pode fugir voando. Hoje, esse veneno é estudado pelo Instituto Butantan. Só pesquisadores com autorização podem entrar, e a espécie está criticamente ameaçada. E aí, você teria coragem de visitar?",
    legenda:
      "🐍 A ilha brasileira onde é PROIBIDO pisar. A Queimada Grande abriga uma cobra que só existe lá, e ela aprendeu a caçar pássaros. Você iria? 👇",
    hashtags: "#curiosidades #vocesabia #brasil #ilhadascobras #natureza #ciencia #fatos",
    fontes: [
      "https://agencia.fapesp.br/livro-celebra-cem-anos-da-descricao-da-jararaca-ilhoa-com-alerta-sobre-conservacao-da-serpente-endemica/37723",
      "https://www.nationalgeographicbrasil.com/animais/2023/03/ilha-das-cobras-o-que-voce-nao-sabia-sobre-a-ilha-tomada-por-serpentes-no-litoral-brasileiro",
      "https://agencia.fapesp.br/sumico-de-jararacas/9642",
    ],
  },
  {
    id: 2,
    slug: "02-agua-viva-imortal",
    titulo: "O animal que não morre de velhice",
    tema: { a: "#1a0f3d", b: "#070418", acc: "#ff7ad9", acc2: "#7ae8ff" },
    hero: "jellyfish",
    cenas: [
      { t: "hook", text: "Esse animal consegue *voltar a ser bebê*", art: "hero" },
      { t: "fact", text: "*Turritopsis dohrnii*", sub: "Uma água-viva menor que a unha do seu mindinho", art: "🔬" },
      { t: "fact", text: "Quando fica ferida, faminta ou velha… ela *não morre*", art: "hero" },
      { t: "fact", text: "Ela transforma o corpo adulto de volta em *pólipo*", sub: "a fase \"bebê\" e recomeça a vida do zero", art: "🔄" },
      { t: "fact", text: "O truque se chama *transdiferenciação*", sub: "uma célula adulta vira outro tipo de célula", art: "🧬" },
      { t: "stat", big: "∞", text: "em teoria, sem limite", sub: "ela pode repetir esse ciclo várias e várias vezes", art: "hero" },
      { t: "fact", text: "Mas ela *não é invencível*", sub: "predadores e doenças ainda podem matá-la", art: "🐟" },
      { t: "cta", text: "Se pudesse rejuvenescer, voltaria pra *qual idade*?", sub: "Responde nos comentários 👇" },
    ],
    narracao:
      "Esse animal consegue voltar a ser bebê. É a Turritopsis dohrnii, uma água-viva menor que a unha do seu mindinho. Quando fica ferida, faminta ou velha, ela não morre: transforma o corpo adulto de volta em pólipo, a fase bebê, e recomeça a vida do zero. O truque se chama transdiferenciação, quando uma célula adulta vira outro tipo de célula. Em teoria, ela pode repetir esse ciclo várias e várias vezes. Mas ela não é invencível: predadores e doenças ainda podem matá-la. Se você pudesse rejuvenescer, voltaria pra qual idade?",
    legenda:
      "🪼 A água-viva \"imortal\" existe e ela literalmente volta a ser bebê quando envelhece. Pra qual idade você voltaria? 👇",
    hashtags: "#curiosidades #vocesabia #aguaviva #imortal #ciencia #biologia #oceano",
    fontes: [
      "https://en.wikipedia.org/wiki/Turritopsis_dohrnii",
      "https://www.sciencefocus.com/nature/immortal-jellyfish/",
    ],
  },
  {
    id: 3,
    slug: "03-tardigrado-espaco",
    titulo: "O bicho que sobreviveu ao vácuo do espaço",
    tema: { a: "#0d1b3a", b: "#03060f", acc: "#ffd34d", acc2: "#6ec1ff" },
    hero: "tardigrade",
    cenas: [
      { t: "hook", text: "Um animal sobreviveu *sem traje* no espaço", art: "hero" },
      { t: "fact", text: "O *tardígrado*, ou \"urso-d'água\"", sub: "Mede cerca de meio milímetro", art: "hero" },
      { t: "fact", text: "Em 2007, a missão *Foton-M3* levou cerca de 3 mil deles para a órbita", art: "🚀" },
      { t: "stat", big: "12 dias", text: "expostos ao vácuo", sub: "e à radiação cósmica, a ~270 km de altitude", art: "☢️" },
      { t: "fact", text: "Resultado: a *maioria sobreviveu*", sub: "e muitos ainda botaram ovos que eclodiram", art: "🥚" },
      { t: "fact", text: "O segredo: eles *secam* e quase desligam o metabolismo", sub: "viram uma bolinha chamada \"tun\"", art: "hero:tun" },
      { t: "fact", text: "Até hoje a ciência *não sabe* explicar tudo", sub: "como alguns aguentaram a radiação UV do Sol", art: "☀️" },
      { t: "cta", text: "O animal mais *resistente* da Terra?", sub: "Comenta outro bicho que você acha mais forte 👇" },
    ],
    narracao:
      "Um animal sobreviveu sem traje no espaço. É o tardígrado, o urso-d'água, que mede cerca de meio milímetro. Em 2007, a missão Foton-M3 levou cerca de 3 mil deles para a órbita da Terra. Eles ficaram 12 dias expostos ao vácuo e à radiação cósmica. Resultado: a maioria sobreviveu, e muitos ainda botaram ovos que eclodiram. O segredo é que eles secam e quase desligam o metabolismo, virando uma bolinha chamada tun. E até hoje a ciência não sabe explicar como alguns aguentaram a radiação ultravioleta do Sol.",
    legenda:
      "🐻 Ele foi pro espaço SEM proteção nenhuma… e voltou vivo. Conhece o tardígrado? Comenta 👇",
    hashtags: "#curiosidades #vocesabia #tardigrado #espaco #ciencia #astronomia #animais",
    fontes: [
      "https://www.esa.int/Our_Activities/Human_Spaceflight/Research/Tiny_animals_survive_exposure_to_space",
      "https://www.space.com/5817-creature-survives-naked-space.html",
      "https://www.sciencedaily.com/releases/2008/09/080908135906.htm",
    ],
  },
  {
    id: 4,
    slug: "04-polvo-alien",
    titulo: "O polvo é praticamente um alienígena",
    tema: { a: "#3a0d24", b: "#12030b", acc: "#ff9d3d", acc2: "#4dd8ff" },
    hero: "octopus",
    cenas: [
      { t: "hook", text: "O polvo tem *3 corações*", art: "hero" },
      { t: "fact", text: "*Dois* bombeiam sangue para as brânquias", sub: "e o terceiro manda sangue para o resto do corpo", art: "🫀" },
      { t: "fact", text: "E o sangue dele é *azul*", sub: "por causa de uma proteína à base de cobre, a hemocianina", art: "💧" },
      { t: "stat", big: "2/3", text: "dos neurônios", sub: "ficam nos braços, não no cérebro", art: "🧠" },
      { t: "fact", text: "Cada braço consegue *agir sozinho*", sub: "explorando e agarrando sem esperar ordens do cérebro", art: "hero" },
      { t: "fact", text: "E ele muda de *cor e textura* em frações de segundo", art: "🎨" },
      { t: "cta", text: "Qual desses fatos te *assustou* mais?", sub: "1, 2 ou 3? Comenta 👇" },
    ],
    narracao:
      "O polvo tem três corações. Dois bombeiam sangue para as brânquias, e o terceiro manda sangue para o resto do corpo. E o sangue dele é azul, por causa de uma proteína à base de cobre chamada hemocianina. Mais: dois terços dos neurônios ficam nos braços, não no cérebro. Por isso cada braço consegue agir sozinho, explorando e agarrando sem esperar ordens. E ele ainda muda de cor e textura em frações de segundo. Qual desses fatos te assustou mais?",
    legenda: "🐙 3 corações, sangue azul e braços que pensam sozinhos. O polvo é um alien? 👽👇",
    hashtags: "#curiosidades #vocesabia #polvo #oceano #animais #ciencia #biologia",
    fontes: [
      "https://www.smithsonianmag.com/science-nature/ten-wild-facts-about-octopuses-they-have-three-hearts-big-brains-and-blue-blood-7625828/",
      "https://www.pbs.org/wnet/nature/group/other-species/octopus/",
    ],
  },
  {
    id: 5,
    slug: "05-cleopatra-lua",
    titulo: "Cleópatra está mais perto da Lua do que das pirâmides",
    tema: { a: "#3b2208", b: "#120a02", acc: "#ffcc4d", acc2: "#9fd3ff" },
    hero: "pyramid",
    cenas: [
      { t: "hook", text: "Cleópatra viveu mais perto da *ida à Lua* do que da construção das pirâmides", art: "hero" },
      {
        t: "timeline",
        text: "Olha a linha do tempo",
        items: [
          { y: "2560 a.C.", l: "Grande Pirâmide", e: "🔺" },
          { y: "69 a.C.", l: "Cleópatra nasce", e: "👑" },
          { y: "1969", l: "Apollo 11 na Lua", e: "🚀" },
        ],
      },
      { t: "stat", big: "≈2.500", text: "anos", sub: "entre a Grande Pirâmide e Cleópatra", art: "🔺" },
      { t: "stat", big: "≈2.000", text: "anos", sub: "entre Cleópatra e a chegada à Lua", art: "🌕" },
      { t: "fact", text: "Para ela, as pirâmides já eram *antiguidades*", sub: "tão antigas quanto ela é para nós", art: "🏛️" },
      { t: "fact", text: "Bônus: ainda existiam *mamutes* quando a pirâmide foi erguida", sub: "os últimos viveram numa ilha no Ártico", art: "🦣" },
      { t: "cta", text: "O tempo é *muito* doido", sub: "Segue pra mais fatos que bugam a cabeça 🤯" },
    ],
    narracao:
      "Cleópatra viveu mais perto da ida à Lua do que da construção das pirâmides. A Grande Pirâmide ficou pronta por volta de 2560 antes de Cristo. Cleópatra nasceu em 69 antes de Cristo. E a Apollo 11 pousou na Lua em 1969. São cerca de 2.500 anos entre a pirâmide e Cleópatra, e só uns 2.000 entre ela e a Lua. Para ela, as pirâmides já eram antiguidades. E tem mais: ainda existiam mamutes quando a pirâmide foi erguida. Os últimos viveram numa ilha no Ártico. O tempo é muito doido.",
    legenda: "👑🚀 Cleópatra está mais perto da Apollo 11 do que das pirâmides. Seu cérebro bugou também? 🤯",
    hashtags: "#curiosidades #vocesabia #historia #egito #cleopatra #piramides #fatos",
    fontes: [
      "https://www.worldatlas.com/articles/so-cleopatra-lived-closer-in-time-to-the-first-lunar-landing-than-the-great-pyramids.html",
      "https://lenz.io/c/cleopatra-moon-landing-great-pyramid-timeline-3a1e5240",
    ],
  },
  {
    id: 6,
    slug: "06-tubaroes-arvores",
    titulo: "Tubarões são mais antigos que as árvores",
    tema: { a: "#06283d", b: "#020c14", acc: "#5ff0d2", acc2: "#9be15d" },
    hero: "shark",
    cenas: [
      { t: "hook", text: "Tubarões são *mais antigos* que as árvores", art: "hero" },
      {
        t: "timeline",
        text: "Milhões de anos atrás",
        items: [
          { y: "~450 mi", l: "1ªs escamas de tubarão", e: "🦈" },
          { y: "~385 mi", l: "1ªs árvores", e: "🌳" },
          { y: "~230 mi", l: "Dinossauros", e: "🦖" },
          { y: "~0,3 mi", l: "Nós, humanos", e: "🧍" },
        ],
      },
      { t: "fact", text: "As primeiras *escamas de tubarão* aparecem em fósseis de ~450 milhões de anos", art: "hero" },
      { t: "fact", text: "As *árvores* de verdade só surgem há ~385 milhões de anos", sub: "na primeira floresta conhecida, em Nova York", art: "🌳" },
      { t: "fact", text: "Eles sobreviveram até à extinção que *acabou com os dinossauros*", art: "☄️" },
      { t: "fact", text: "Detalhe: os tubarões *modernos* surgiram há ~195 milhões de anos", sub: "mas a linhagem é bem mais velha que as florestas", art: "🧬" },
      { t: "cta", text: "Sabia dessa?", sub: "Marca alguém que tem medo de tubarão 🦈" },
    ],
    narracao:
      "Tubarões são mais antigos que as árvores. As primeiras escamas de tubarão aparecem em fósseis de cerca de 450 milhões de anos. Já as árvores de verdade só surgem há uns 385 milhões de anos. Os dinossauros, há 230 milhões. E nós, humanos, há só 300 mil anos. Os tubarões sobreviveram até à extinção que acabou com os dinossauros. Um detalhe: os tubarões modernos surgiram há cerca de 195 milhões de anos, mas a linhagem deles é bem mais velha que as florestas.",
    legenda: "🦈🌳 Antes de existir UMA árvore na Terra, já existiam tubarões. Marca quem tem medo deles 👇",
    hashtags: "#curiosidades #vocesabia #tubarao #evolucao #ciencia #oceano #fatos",
    fontes: [
      "https://www.livescience.com/animals/sharks/are-sharks-really-older-than-trees",
      "https://www.smithsonianmag.com/smart-news/respect-sharks-are-older-than-trees-3818/",
    ],
  },
  {
    id: 7,
    slug: "07-mel-eterno",
    titulo: "O alimento que quase nunca estraga",
    tema: { a: "#3d2400", b: "#140b00", acc: "#ffb627", acc2: "#fff1c1" },
    hero: "honey",
    cenas: [
      { t: "hook", text: "O alimento que *quase nunca* estraga", art: "hero" },
      { t: "stat", big: "3.000", text: "anos", sub: "idade de potes de mel achados em tumbas egípcias", art: "🏺" },
      { t: "fact", text: "O mel tem *pouquíssima água*", sub: "micróbios que caem nele são \"secos\" por osmose", art: "🦠" },
      { t: "stat", big: "pH 3,2–4,5", text: "ácido", sub: "o suficiente para barrar muitas bactérias", art: "🧪" },
      { t: "fact", text: "As abelhas ainda adicionam uma enzima que gera *água oxigenada*", sub: "(peróxido de hidrogênio)", art: "🐝" },
      { t: "fact", text: "Cristalizou? *Não estragou!*", sub: "Banho-maria e pronto. Só mantenha o pote bem fechado", art: "hero" },
      { t: "fact", text: "⚠️ Bebês com *menos de 1 ano* não devem comer mel", sub: "risco de botulismo infantil", art: "👶" },
      { t: "cta", text: "Você jogava mel cristalizado *fora*?", sub: "Seja sincero 👇" },
    ],
    narracao:
      "Esse é o alimento que quase nunca estraga. Arqueólogos encontraram potes de mel em tumbas egípcias com cerca de 3 mil anos. O segredo: o mel tem pouquíssima água, então micróbios que caem nele são secos por osmose. Ele também é ácido, com pH entre 3,2 e 4,5. E as abelhas ainda adicionam uma enzima que gera água oxigenada. Cristalizou? Não estragou: é só banho-maria. Só mantenha o pote bem fechado. E atenção: bebês com menos de um ano não devem comer mel. Você jogava mel cristalizado fora?",
    legenda: "🍯 Mel cristalizado NÃO está estragado! E tem pote de 3 mil anos pra provar. Você jogava fora? 👇",
    hashtags: "#curiosidades #vocesabia #mel #alimentacao #ciencia #egito #dicas",
    fontes: [
      "https://www.beeculture.com/honeys-eternal-shelf-life/",
      "https://www.smithsonianmag.com/science-nature/the-science-behind-honeys-eternal-shelf-life-1218690/",
    ],
  },
  {
    id: 8,
    slug: "08-formiga-zumbi",
    titulo: "O fungo que transforma formigas em zumbis",
    tema: { a: "#16300c", b: "#060f03", acc: "#d6ff3d", acc2: "#ff8a3d" },
    hero: "ant",
    cenas: [
      { t: "hook", text: "Existe um fungo que transforma formigas em *zumbis*", art: "hero" },
      { t: "fact", text: "*Ophiocordyceps*", sub: "ataca formigas-carpinteiras em florestas tropicais", art: "🍄" },
      { t: "fact", text: "A formiga infectada sai do ninho e começa a *vagar sem rumo*", art: "hero" },
      { t: "fact", text: "Perto do *meio-dia*, ela sobe numa planta e morde a nervura de uma folha", art: "🌿" },
      { t: "fact", text: "Os músculos da mandíbula atrofiam e a *mordida da morte* trava", sub: "ela fica presa ali para sempre", art: "🔒" },
      { t: "fact", text: "Dias depois, uma *haste brota da cabeça*", sub: "e solta esporos sobre as formigas lá embaixo", art: "hero:sprout" },
      { t: "fact", text: "Calma: esse fungo *não infecta humanos*", sub: "isso só acontece na ficção 😮‍💨", art: "🧍" },
      { t: "cta", text: "A natureza é *assustadora*", sub: "Segue pra parte 2 🍄" },
    ],
    narracao:
      "Existe um fungo que transforma formigas em zumbis. Ele se chama Ophiocordyceps e ataca formigas-carpinteiras em florestas tropicais. A formiga infectada sai do ninho e começa a vagar sem rumo. Perto do meio-dia, ela sobe numa planta e morde a nervura de uma folha. Os músculos da mandíbula atrofiam, e a mordida da morte trava: ela fica presa ali para sempre. Dias depois, uma haste brota da cabeça e solta esporos sobre as formigas lá embaixo. Calma: esse fungo não infecta humanos. Isso só acontece na ficção.",
    legenda: "🍄🐜 Isso não é filme: um fungo controla formigas até a última mordida. A natureza é assustadora 👇",
    hashtags: "#curiosidades #vocesabia #fungo #formiga #zumbi #natureza #ciencia",
    fontes: [
      "https://pmc.ncbi.nlm.nih.gov/articles/PMC3118224/",
      "https://www.nationalgeographic.com/animals/article/cordyceps-zombie-fungus-takes-over-ants",
      "https://www.sciencenews.org/article/death-grip-fungus-made-me-do-it",
    ],
  },
  {
    id: 9,
    slug: "09-estrela-de-neutrons",
    titulo: "Uma colher de chá que pesa 1 bilhão de toneladas",
    tema: { a: "#120a33", b: "#030112", acc: "#8fb6ff", acc2: "#ff6bd5" },
    hero: "neutron",
    cenas: [
      { t: "hook", text: "Uma colher de chá disso pesaria *1 bilhão de toneladas*", art: "hero" },
      { t: "fact", text: "É matéria de uma *estrela de nêutrons*", sub: "o que sobra quando uma estrela gigante explode", art: "💥" },
      {
        t: "compare",
        text: "Imagine:",
        items: [
          { e: "☀️", big: "+ massa", l: "que o Sol inteiro" },
          { e: "🏙️", big: "~20 km", l: "de diâmetro: uma cidade" },
        ],
      },
      { t: "stat", big: "1 bilhão", text: "de toneladas", sub: "numa colherzinha de chá", art: "🥄" },
      { t: "fact", text: "Isso é cerca do *dobro do peso* de todos os humanos da Terra juntos", art: "🌍" },
      { t: "stat", big: "716", text: "voltas por segundo", sub: "a estrela de nêutrons mais rápida já medida", art: "hero" },
      { t: "cta", text: "O universo é *absurdo*", sub: "Comenta 🤯 se seu cérebro explodiu" },
    ],
    narracao:
      "Uma colher de chá disso pesaria um bilhão de toneladas. É matéria de uma estrela de nêutrons, o que sobra quando uma estrela gigante explode. Imagine: mais massa que o Sol inteiro, espremida numa bola de uns 20 quilômetros, o tamanho de uma cidade. Uma colherzinha dessa matéria pesa cerca do dobro de todos os humanos da Terra juntos. E a mais rápida já medida gira 716 vezes por segundo. O universo é absurdo.",
    legenda: "🥄✨ Uma colher disso pesa mais que TODA a humanidade junta. O universo é absurdo 🤯",
    hashtags: "#curiosidades #vocesabia #espaco #astronomia #universo #estrelas #ciencia",
    fontes: [
      "https://www.space.com/22180-neutron-stars.html",
      "https://www.astronomy.com/astronomy-for-beginners/astronomy-101-neutron-stars/",
    ],
  },
  {
    id: 10,
    slug: "10-vombate-cubo",
    titulo: "O animal que faz cocô em formato de cubo",
    tema: { a: "#2e1d12", b: "#0f0905", acc: "#ffb38a", acc2: "#9ee6a8" },
    hero: "wombat",
    cenas: [
      { t: "hook", text: "Existe um animal que faz cocô em formato de *cubo*", art: "hero" },
      { t: "fact", text: "É o *vombate*", sub: "um marsupial fofinho da Austrália", art: "🇦🇺" },
      { t: "stat", big: "80 a 100", text: "cubinhos", sub: "por noite", art: "🧊" },
      { t: "fact", text: "Para quê? Ele usa os cubos para *marcar território*", sub: "em pedras e troncos, e o formato não deixa rolar", art: "🪨" },
      { t: "fact", text: "O formato nasce *dentro do intestino*", sub: "faixas rígidas e flexíveis moldam as quinas", art: "hero:cube" },
      { t: "fact", text: "A descoberta ganhou o *Ig Nobel* de Física em 2019", sub: "o prêmio das pesquisas que fazem rir e depois pensar", art: "🏆" },
      { t: "cta", text: "Você *sabia* dessa?", sub: "Manda pra alguém que precisa saber disso 😂" },
    ],
    narracao:
      "Existe um animal que faz cocô em formato de cubo. É o vombate, um marsupial da Austrália. Ele faz de 80 a 100 cubinhos por noite. Para quê? Ele usa os cubos para marcar território em pedras e troncos, e o formato não deixa rolar. O formato nasce dentro do intestino, onde faixas mais rígidas e mais flexíveis moldam as quinas. A descoberta ganhou o prêmio Ig Nobel de Física em 2019. Você sabia dessa?",
    legenda: "🧊💩 Sim, existe cocô quadrado. E rendeu até prêmio científico. Manda pra alguém 😂",
    hashtags: "#curiosidades #vocesabia #vombate #australia #animais #ciencia #engracado",
    fontes: [
      "https://www.livescience.com/why-wombats-have-cubed-poop.html",
      "https://newatlas.com/biology/square-wombat-poo-method-replicated",
    ],
  },
];

// Duração automática de cada cena pelo tamanho do texto (tempo de leitura).
function sceneDuration(c) {
  if (c.d) return c.d;
  const chars = (c.text || "").length + (c.sub || "").length * 0.8 + (c.big || "").length;
  let d = 2.6 + chars / 17;
  if (c.t === "timeline") d = 2.4 + c.items.length * 1.35;
  if (c.t === "compare") d = 6.0;
  if (c.t === "hook") d = Math.max(d, 3.6);
  if (c.t === "cta") d = Math.max(d, 4.2);
  return Math.round(Math.min(Math.max(d, 3.4), 7.2) * 10) / 10;
}

// Se a narração existir (voz/durs.js), cada cena dura o tempo da fala.
const VOZ_LEAD = 0.2;
function timeline(video) {
  let t = 0;
  const voz = (typeof VOZ !== "undefined" ? VOZ : (() => { try { return require("./voz/durs.js").VOZ; } catch (e) { return null; } })());
  const vd = voz && voz[video.id];
  return video.cenas.map((c, i) => {
    let d = sceneDuration(c);
    if (vd) d = Math.round((vd[i] + VOZ_LEAD + 0.4 + (i === video.cenas.length - 1 ? 1.6 : 0)) * 100) / 100;
    const s = { ...c, start: t, dur: d };
    t += d;
    return s;
  });
}

if (typeof module !== "undefined") module.exports = { VIDEOS, sceneDuration, timeline };
