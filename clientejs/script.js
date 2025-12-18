// Referências aos elementos do DOM
const pokedexGrid = document.getElementById('pokedex-grid');
const searchInput = document.getElementById('searchInput');
const loader = document.getElementById('loader');
const modal = document.getElementById('pokemon-modal');
const modalContent = document.getElementById('modal-content');

// Armazenará todos os dados dos Pokémon para a pesquisa
let allPokemonData = [];
const POKEMON_COUNT = 151; // Vamos buscar a primeira geração

/**
 * Mapeamento de nomes de stats para abreviações mais limpas
 */
const statNameMapping = {
    'hp': 'HP',
    'attack': 'Attack',
    'defense': 'Defense',
    'special-attack': 'Sp. Atk',
    'special-defense': 'Sp. Def',
    'speed': 'Speed'
};

/**
 * Função principal que busca os dados da API
 */
const fetchAllPokemon = async () => {
    try {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon?limit=${POKEMON_COUNT}`);
        const data = await response.json();
        const pokemonPromises = data.results.map(pokemon => fetch(pokemon.url).then(res => res.json()));
        
        allPokemonData = await Promise.all(pokemonPromises);
        allPokemonData.sort((a, b) => a.id - b.id); // Garante a ordem correta
        
        loader.style.display = 'none';
        displayPokemon(allPokemonData);

    } catch (error) {
        console.error("Falha ao buscar dados dos Pokémon:", error);
        loader.innerHTML = "<p class='text-red-500'>Erro ao carregar os dados. Tente recarregar a página.</p>";
    }
};

/**
 * Exibe os Pokémon na grade com o novo design
 */
const displayPokemon = (pokemonList) => {
    pokedexGrid.innerHTML = '';
    
    pokemonList.forEach(pokemon => {
        const primaryType = pokemon.types[0].type.name;
        const cardColor = getTypeColor(primaryType);
        const pokemonSprite = pokemon.sprites.versions['generation-v']['black-white'].animated.front_default || pokemon.sprites.other['official-artwork'].front_default || pokemon.sprites.front_default;

        const typesHtml = pokemon.types.map(typeInfo =>
            `<span class="text-xs font-semibold text-white px-2 py-1 rounded-full shadow-md" style="background-color: rgba(255, 255, 255, 0.2);">${typeInfo.type.name}</span>`
        ).join(' ');
        
        const card = document.createElement('div');
        card.className = 'relative rounded-xl shadow-lg p-4 flex flex-col items-center justify-center cursor-pointer transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 text-white overflow-hidden h-48';
        
        card.style.background = `linear-gradient(135deg, ${adjustColor(cardColor, 20)}, ${adjustColor(cardColor, -20)})`;

        card.innerHTML = `
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Pok%C3%A9_Ball_icon.svg" class="absolute -bottom-4 -right-4 w-28 h-28 opacity-10 rotate-12" alt="Pokeball watermark">
            <span class="absolute top-2 right-3 font-bold text-lg" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">#${pokemon.id.toString().padStart(3, '0')}</span>
            <img src="${pokemonSprite}" alt="${pokemon.name}" class="w-20 h-20 z-10" style="filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.4));">
            <h2 class="text-xl font-bold capitalize mt-2 z-10 text-shadow-sm text-center">${pokemon.name}</h2>
            <div class="flex gap-2 mt-2 z-10">
                ${typesHtml}
            </div>
        `;
        
        card.addEventListener('click', () => showPokemonDetails(pokemon));
        pokedexGrid.appendChild(card);
    });
};

/**
 * Filtra os Pokémon com base na entrada de pesquisa
 */
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredPokemon = allPokemonData.filter(pokemon => 
        pokemon.name.toLowerCase().includes(searchTerm) || 
        pokemon.id.toString().padStart(3, '0').includes(searchTerm)
    );
    displayPokemon(filteredPokemon);
});

/**
 * Busca dados da cadeia de evolução e a exibe
 */
const showPokemonDetails = async (pokemon) => {
    document.body.style.overflow = 'hidden';

    try {
        const speciesResponse = await fetch(pokemon.species.url);
        const speciesData = await speciesResponse.json();
        const evolutionChainResponse = await fetch(speciesData.evolution_chain.url);
        const evolutionChainData = await evolutionChainResponse.json();
        await displayModal(pokemon, evolutionChainData);
    } catch (error) {
        console.error("Erro ao buscar detalhes do Pokémon:", error);
        modalContent.innerHTML = "<p class='p-6'>Não foi possível carregar os detalhes.</p>";
    }
    modal.classList.remove('hidden');
};

/**
 * Constrói e exibe o modal com o novo design
 */
const displayModal = (pokemon, evolutionChain) => {
    const primaryType = pokemon.types[0].type.name;
    const modalColor = getTypeColor(primaryType);

    const typesHtml = pokemon.types.map(typeInfo => 
        `<span class="px-3 py-1 text-sm font-semibold text-white rounded-full shadow-md" style="background-color: rgba(255, 255, 255, 0.2);">${typeInfo.type.name}</span>`
    ).join(' ');

    const statsHtml = pokemon.stats.map(stat => {
        const statName = statNameMapping[stat.stat.name] || stat.stat.name.replace('-', ' ');
        const statPercentage = (stat.base_stat / 255) * 100; 
        
        return `
        <div class="grid grid-cols-12 items-center gap-2 text-sm">
            <span class="col-span-4 font-semibold text-gray-500">${statName}</span>
            <span class="col-span-2 font-bold text-gray-800 text-right">${stat.base_stat}</span>
            <div class="col-span-6 bg-gray-200 rounded-full h-2">
                <div class="h-2 rounded-full" style="width: ${statPercentage}%; background-color: ${modalColor};"></div>
            </div>
        </div>
        `
    }).join('');

    const evolutionHtml = parseEvolutionChain(evolutionChain.chain);

    modalContent.innerHTML = `
        <div class="relative p-6 rounded-t-2xl text-white" style="background: linear-gradient(135deg, ${adjustColor(modalColor, 20)}, ${adjustColor(modalColor, -20)})">
            
            <button id="close-modal-inner" class="absolute top-4 right-4 w-9 h-9 flex items-center justify-center bg-white/20 rounded-full hover:bg-white/40 transition-colors z-20">
                <span class="text-2xl font-bold">&times;</span>
            </button>
            
            <div class="flex flex-col sm:flex-row items-center gap-4">
                <div class="relative flex-shrink-0">
                     <img src="${pokemon.sprites.other['official-artwork'].front_default}" alt="${pokemon.name}" class="w-32 h-32 sm:w-40 sm:h-40" style="filter: drop-shadow(2px 4px 8px rgba(0,0,0,0.4));">
                </div>
                <div class="text-center sm:text-left z-10">
                    <p class="font-bold text-lg opacity-80">#${pokemon.id.toString().padStart(3, '0')}</p>
                    <h2 class="text-4xl font-black capitalize text-shadow">${pokemon.name}</h2>
                    <div class="flex justify-center sm:justify-start gap-2 mt-3">${typesHtml}</div>
                </div>
            </div>
        </div>
        
        <div class="p-6 bg-white rounded-b-2xl">
            <div>
                <h3 class="font-bold text-xl mb-4 text-gray-800 border-b pb-2">Estatísticas</h3>
                <div class="space-y-3">${statsHtml}</div>
            </div>
            
            <div class="mt-6">
                 <h3 class="font-bold text-xl mb-4 text-gray-800 border-b pb-2">Evoluções</h3>
                 <div class="flex justify-around items-center gap-2 flex-wrap">${evolutionHtml}</div>
            </div>
        </div>
    `;
};

/**
 * Função recursiva para percorrer e montar o HTML da cadeia de evolução
 */
const parseEvolutionChain = (chain) => {
    let html = `
        <div class="flex flex-col items-center text-center p-2">
            <img 
                src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${getPokemonIdFromUrl(chain.species.url)}.png" 
                class="w-24 h-24 mx-auto hover:scale-110 transition-transform cursor-pointer"
                alt="${chain.species.name}"
                onclick="changePokemonInModal('${chain.species.name}')"
            >
            <p class="capitalize font-semibold mt-1">${chain.species.name}</p>
        </div>
    `;

    if (chain.evolves_to.length > 0) {
        html += `<div class="flex items-center justify-center text-gray-400 text-2xl font-light self-center mx-2">&gt;</div>`;
        if (chain.evolves_to.length > 1) {
            html += '<div class="flex flex-col gap-4">';
            chain.evolves_to.forEach(evolution => {
                html += parseEvolutionChain(evolution);
            });
            html += '</div>';
        } else {
             html += parseEvolutionChain(chain.evolves_to[0]);
        }
    }
    return html;
};

/**
 * Permite clicar na evolução para ver seus detalhes
 */
const changePokemonInModal = (pokemonName) => {
    const newPokemon = allPokemonData.find(p => p.name === pokemonName);
    if (newPokemon) {
        showPokemonDetails(newPokemon);
    }
}

// Funções Auxiliares
const getPokemonIdFromUrl = (url) => url.split('/').filter(Boolean).pop();

const getTypeColor = (type) => {
    const colors = {
        fire: '#F08030', grass: '#78C850', water: '#6890F0', bug: '#A8B820',
        normal: '#A8A878', poison: '#A040A0', electric: '#F8D030', ground: '#E0C068',
        fairy: '#EE99AC', fighting: '#C03028', psychic: '#F85888', rock: '#B8A038',
        ghost: '#705898', ice: '#98D8D8', dragon: '#7038F8', steel: '#B8B8D0', dark: '#705848', flying: '#A890F0'
    };
    return colors[type] || '#68A090';
};

const adjustColor = (hex, amount) => {
    return '#' + hex.replace(/^#/, '').replace(/../g, color => ('0'+Math.min(255, Math.max(0, parseInt(color, 16) + amount)).toString(16)).substr(-2));
};

// Evento de fechar o modal
modal.addEventListener('click', (e) => {
    if (e.target.id === 'pokemon-modal' || e.target.closest('#close-modal-inner')) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
});

// Inicia a aplicação
fetchAllPokemon();