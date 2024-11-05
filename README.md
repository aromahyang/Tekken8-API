# Tekken 8 API v1.0.0

This API provides Tekken 8 move data and notation generation tools, sourced from WavuWiki. It includes features to retrieve and search movesets, and a notation maker that detects starter frames and generates button notation images.

# Features
- **Notation Maker**: Detects the starter frame for any move and creates images with the button notation.
- **Get All Movesets**: Fetches the complete list of moves available in Tekken 8.
- **Search Moveset**: Allows users to search for specific movesets based on notation.

## API Reference

#### Notation Maker

```http
  POST /notation
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `character_name` | `string` | *Character Name of Tekken 8 |
| `notation` | `string` | *Your notation |

#### Find moveset

```http
  POST /findmove
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `character_name`      | `string` | *Character Name of Tekken 8 |
| `notation` | `string` | Notation to find |

#### Get moveset

```http
  POST /movetable
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `character_name`      | `string` | *Character Name of Tekken 8 |
| `notation` | `string` | Notation to find |

## Usage/Examples

#### Notation Maker:
```http
POST /notation
{
    "character_name": "lee",
    "notation": "b,B+4 dash b,3,3 f,4:1 b,1:1+2"
}
```
![Notation Maker Example](app/public/example/response.png)

#### Get movetable:
```http
POST /movetable
{
    "character_name": "kazuya"
}
```
```json
{
    "total_data": 124,
    "data": [
        {
            "moveset": "Kazuya-1",
            "name_move": "Jab",
            "startup": "i10",
            "hit_properties": "h",
            "damage": "5",
            "on_block": "+1",
            "on_hit": "+8",
            "on_CH": "",
            "states": "",
            "notes": "Recovers 2f faster on hit or block (t27 r17)"
        },
        {
            "moveset": "Kazuya-1,1",
            "name_move": "",
            "startup": ",i15",
            "hit_properties": ",h",
            "damage": ",6",
            "on_block": "-1",
            "on_hit": "+8",
            "on_CH": "",
            "states": "",
            "notes": "JailsCombo from 1st hit"
        },
        ...
    ]
}
```


#### Findmove:
```http
POST /findmove
{
    "character_name": "claudio",
    "notation": "1"
}
```
Output will be:
```json
{
    "total_data": 1,
    "data": [
        {
            "moveset": "Claudio-1",
            "name_move": "Jab",
            "startup": "i10",
            "hit_properties": "h",
            "damage": "5",
            "on_block": "+1",
            "on_hit": "+8",
            "on_CH": "",
            "states": "",
            "notes": "Recovers 2f faster on hit or block (t27 r17)"
        }
    ]
}
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/dammar01/Tekken8-API
```

Go to the project directory

```bash
  cd Tekken8-API
```

Add venv

```bash
  py -m venv venv
```

Activate venv

```bash
  venv\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app --reload
```


## Contributing

Contributions are always welcome!

Feel free to customize any section to better fit your project structure!









## Feedback

If you have any feedback, please reach out to me at dammar.s011@gmail.com or DM me at instagram [@dmmrs_a](https://www.instagram.com/dmmrs_a/)


## Acknowledgements

 - [WavuWiki](https://wavu.wiki/t/Main_Page)

## License
This project is licensed under the Mozilla Public License 2.0 (MPL-2.0). For more details, see the [LICENSE](LICENSE) file

