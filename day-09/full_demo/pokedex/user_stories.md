# User Stories

- User will be able to see displayed pokemon
    - User will be able to see types and stats
    - User will be able to see pokemon evolutions
- User will be able to see a picture of that pokemon
- User will be able to search for a pokemon
- User will be able to favorite a pokemon and see their favorited pokemon
    - This is per user
    - Unfavorite that pokemon
    - Track whether you've caught your fav pokemon or not

# Models

- User - username & password
- Favorite - user.foreignkey, pokemon.foreignkey, caught
- Pokemon - name, pokemon_id, types
- PokemonType - name

User ----< Favorite >---- Pokemon ---<>--- PokemonType