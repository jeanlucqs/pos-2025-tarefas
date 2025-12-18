import { POKEMON_COUNT } from './utils.js';

export const fetchAllPokemon = async () => {
    try {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon?limit=${POKEMON_COUNT}`);
        const data = await response.json();
        // Mapeia cada resultado para uma nova promessa de busca de detalhes
        const pokemonPromises = data.results.map(p => fetch(p.url).then(res => res.json()));
        
        const allData = await Promise.all(pokemonPromises);
        return allData.sort((a, b) => a.id - b.id);
    } catch (error) {
        throw new Error("Falha ao conectar com o Professor Carvalho. Tente novamente.");
    }
};

export const fetchEvolutionChain = async (pokemon) => {
    const speciesRes = await fetch(pokemon.species.url);
    const speciesData = await speciesRes.json();
    const evolutionRes = await fetch(speciesData.evolution_chain.url);
    return await evolutionRes.json();
};