import { getTypeColor, adjustColor, statNameMapping } from './utils.js';

export const domElements = {};

export const createInitialShell = () => {
    document.body.innerHTML = `
        <header class="bg-red-600 p-6 shadow-xl sticky top-0 z-50">
            <div class="container mx-auto flex justify-between items-center">
                <h1 class="text-white text-3xl font-black tracking-tighter">POKÉDEX V2</h1>
                <input id="searchInput" type="text" placeholder="Buscar Pokémon..." 
                       class="px-4 py-2 rounded-lg bg-white/20 text-white placeholder-white/70 outline-none border border-white/30 focus:bg-white focus:text-gray-800 transition-all">
            </div>
        </header>

        <main class="container mx-auto p-6">
            <div id="pokedex-grid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6"></div>
            <div id="loader" class="text-center py-20 text-xl font-bold text-gray-400">Carregando dados...</div>
        </main>

        <div id="pokemon-modal" class="fixed inset-0 bg-black/90 hidden z-[100] flex items-center justify-center p-4 backdrop-blur-sm">
            <div id="modal-content" class="bg-white rounded-3xl max-w-lg w-full overflow-hidden shadow-2xl"></div>
        </div>
    `;

    domElements.grid = document.getElementById('pokedex-grid');
    domElements.searchInput = document.getElementById('searchInput');
    domElements.loader = document.getElementById('loader');
    domElements.modal = document.getElementById('pokemon-modal');
    domElements.modalContent = document.getElementById('modal-content');
};

export const displayPokemonCards = (pokemonList, onCardClick) => {
    domElements.grid.innerHTML = '';
    pokemonList.forEach(pokemon => {
        const color = getTypeColor(pokemon.types[0].type.name);
        const card = document.createElement('div');
        card.className = 'relative p-4 rounded-2xl cursor-pointer hover:scale-105 transition-transform text-white overflow-hidden shadow-lg';
        card.style.background = `linear-gradient(180deg, ${color}, ${adjustColor(color, -30)})`;
        
        card.innerHTML = `
            <span class="absolute top-2 right-4 opacity-40 font-bold text-xl">#${pokemon.id}</span>
            <img src="${pokemon.sprites.front_default}" class="w-24 h-24 mx-auto relative z-10" alt="${pokemon.name}">
            <h2 class="text-center capitalize font-bold text-lg mt-2">${pokemon.name}</h2>
        `;
        card.addEventListener('click', () => onCardClick(pokemon));
        domElements.grid.appendChild(card);
    });
};