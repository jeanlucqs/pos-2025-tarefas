import * as api from './src/pokeApi.js';
import * as dom from './src/dom.js';

let allPokemon = [];

async function handleCardClick(pokemon) {
    try {
        const evolution = await api.fetchEvolutionChain(pokemon);
        // Exemplo simplificado de preenchimento do modal
        dom.domElements.modalContent.innerHTML = `
            <div class="p-8 text-center" style="background: ${dom.getTypeColor(pokemon.types[0].type.name)}">
                <img src="${pokemon.sprites.other['official-artwork'].front_default}" class="w-48 h-48 mx-auto">
                <h2 class="text-4xl font-black text-white capitalize mt-4">${pokemon.name}</h2>
            </div>
            <div class="p-6">
                <button id="close-modal" class="w-full py-3 bg-gray-100 rounded-xl font-bold text-gray-600 hover:bg-gray-200">FECHAR</button>
            </div>
        `;
        dom.domElements.modal.classList.remove('hidden');
    } catch (e) {
        console.error(e);
    }
}

function setupEventListeners() {
    dom.domElements.searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allPokemon.filter(p => p.name.includes(term) || p.id.toString().includes(term));
        dom.displayPokemonCards(filtered, handleCardClick);
    });

    dom.domElements.modal.addEventListener('click', (e) => {
        if(e.target.id === 'pokemon-modal' || e.target.id === 'close-modal') {
            dom.domElements.modal.classList.add('hidden');
        }
    });
}

async function init() {
    dom.createInitialShell();
    setupEventListeners();

    try {
        allPokemon = await api.fetchAllPokemon();
        dom.domElements.loader.classList.add('hidden');
        dom.displayPokemonCards(allPokemon, handleCardClick);
    } catch (error) {
        dom.domElements.loader.innerHTML = `<p class="text-red-500">${error.message}</p>`;
    }
}

init();