# Tekken 8 API v1.0.2

This API provides Tekken 8 move data and notation generation tools, sourced from WavuWiki. It includes features to retrieve and search movesets, and a notation maker that detects starter frames and generates button notation images.

# Features

- **Notation Maker**: Detects the starter frame for any move and creates images with the button notation.
- **Get All Movesets**: Fetches the complete list of moves available in Tekken 8.
- **Search Moveset**: Allows users to search for specific movesets based on notation.

## API Reference

#### Notation Maker

```json
  POST /notation
```

| Parameter        | Type     | Description                  |
| :--------------- | :------- | :--------------------------- |
| `character_name` | `string` | \*Character Name of Tekken 8 |
| `notation`       | `string` | \*Your notation              |

##### Notation reference

| Raw notation  | How to request | Description                                              | Output Image                         |
| :------------ | :------------- | :------------------------------------------------------- | :----------------------------------- |
| `1`           | `1`            | `Left Punch`                                             | ![ ](app/public/button/1.png)        |
| `2`           | `2`            | `Right Punch`                                            | ![ ](app/public/button/2.png)        |
| `3`           | `3`            | `Left kick`                                              | ![ ](app/public/button/3.png)        |
| `4`           | `4`            | `Right kick`                                             | ![ ](app/public/button/4.png)        |
| `1+2`         | `1+2`          | `Left punch and right punch, pressed together.`          | ![ ](app/public/button/1+2.png)      |
| `1+2+3`       | `1+2+3`        | `Left and right punch, then left kick pressed together`  | ![ ](app/public/button/1+2+3.png)    |
| `1+2+3+4`     | `1+2+3+4`      | `Ki Charge`                                              | ![ ](app/public/button/1+2+3+4.png)  |
| `1+3`         | `1+3`          | `Left Punch and left kick pressed together`              | ![ ](app/public/button/1+3.png)      |
| `1+3+4`       | `1+3+4`        | `Left punch, then left and right kick pressed together`  | ![ ](app/public/button/1+3+4.png)    |
| `1+2+4`       | `1+2+4`        | `Left and right punch, then right kick pressed together` | ![ ](app/public/button/1+2+4.png)    |
| `1+4`         | `1+4`          | `Left Punch and right kick pressed together`             | ![ ](app/public/button/1+4.png)      |
| `2+3`         | `2+3`          | `Right Punch and left kick pressed together`             | ![ ](app/public/button/2+3.png)      |
| `2+3+4`       | `2+3+4`        | `Right Punch, then left and right kick pressed together` | ![ ](app/public/button/2+3+4.png)    |
| `2+4`         | `2+4`          | `Right Punch and right kick pressed together`            | ![ ](app/public/button/2+4.png)      |
| `3+4`         | `3+4`          | `Left and right kick pressed together`                   | ![ ](app/public/button/3+4.png)      |
| `u`           | `u`            | `Up`                                                     | ![ ](app/public/button/u.png)        |
| `U`           | `U`            | `Up (Hold)`                                              | ![ ](app/public/button/^u.png)       |
| `ub`          | `ub`           | `Up and backward`                                        | ![ ](app/public/button/ub.png)       |
| `UB`          | `UB`           | `Up and backward (Hold)`                                 | ![ ](app/public/button/^u^b.png)     |
| `uf`          | `uf`           | `Up and forward`                                         | ![ ](app/public/button/uf.png)       |
| `d`           | `d`            | `Down`                                                   | ![ ](app/public/button/d.png)        |
| `D`           | `D`            | `Down (hold)`                                            | ![ ](app/public/button/^d.png)       |
| `db`          | `db`           | `Down and backward`                                      | ![ ](app/public/button/db.png)       |
| `DB`          | `DB`           | `Down and backward (hold)`                               | ![ ](app/public/button/^d^b.png)     |
| `df`          | `df`           | `Down and forward`                                       | ![ ](app/public/button/df.png)       |
| `DF`          | `DF`           | `Down and forward (hold)`                                | ![ ](app/public/button/^d^f.png)     |
| `b`           | `b`            | `Back`                                                   | ![ ](app/public/button/b.png)        |
| `B`           | `B`            | `Back (Hold)`                                            | ![ ](app/public/button/^b.png)       |
| `f`           | `f`            | `Forward`                                                | ![ ](app/public/button/f.png)        |
| `F`           | `F`            | `Forward (hold)`                                         | ![ ](app/public/button/^f.png)       |
| `cc`          | `cc`           | `Crouch cancel (u~n)`                                    | ![ ](app/public/button/cc.png)       |
| `BB!`         | `BB!`          | `Balcony break`                                          | ![ ](app/public/button/^b^b!.png)    |
| `CD`          | `CD`           | `Crouch dash`                                            | ![ ](app/public/button/^c^d.png)     |
| `CH`          | `CH`           | `Counter Hit`                                            | ![ ](app/public/button/^c^h.png)     |
| `FB!`         | `FB!`          | `Floor Break`                                            | ![ ](app/public/button/^f^b!.png)    |
| `FBl!`        | `FBl!`         | `Floor Blast`                                            | ![ ](app/public/button/^f^bl!.png)   |
| `FC!`         | `FC!`          | `Full Crouch`                                            | ![ ](app/public/button/^f^c.png)     |
| `H`           | `H!`           | `During Heat`                                            | ![ ](app/public/button/^h.png)       |
| `RA`          | `R`            | `Rage Art`                                               | ![ ](app/public/button/^r.png)       |
| `SS`          | `SS`           | `Side Step`                                              | ![ ](app/public/button/^s^s.png)     |
| `SSL`         | `SSL`          | `Side Step Left`                                         | ![ ](app/public/button/^s^s^l.png)   |
| `SSR`         | `SSR`          | `Side Step Right`                                        | ![ ](app/public/button/^s^s^r.png)   |
| `SWL`         | `SWL`          | `Side Walk Left`                                         | ![ ](app/public/button/^s^w^l.png)   |
| `SWR`         | `SWR`          | `Side Walk Right`                                        | ![ ](app/public/button/^s^w^r.png)   |
| `T!`          | `T!`           | `Tornado`                                                | ![ ](app/public/button/^t!.png)      |
| `UF`          | `UF`           | `Up and forward (Hold)`                                  | ![ ](app/public/button/^u^f.png)     |
| `W!`          | `W!`           | `Wall Splat, Wall Bounce`                                | ![ ](app/public/button/^w!.png)      |
| `WB!`         | `WB!`          | `Wall Break`                                             | ![ ](app/public/button/^w^b!.png)    |
| `WBl!`        | `WBl!`         | `Wall Blast`                                             | ![ ](app/public/button/^w^bl!.png)   |
| `WBo!`        | `WBo!`         | `Wall Bound`                                             | ![ ](app/public/button/^w^bo!.png)   |
| `WR`          | `WR`           | `While Running`                                          | ![ ](app/public/button/^w^r.png)     |
| `WS`          | `WS`           | `While Standing`                                         | ![ ](app/public/button/^w^s.png)     |
| `DASH`        | `dash`         | `Dash (f,f)`                                             | ![ ](app/public/button/dash.png)     |
| `Deep Dash`   | `ddash`        | `DEEP DASH`                                              | ![ ](app/public/button/ddash.png)    |
| `iWS`         | `iWS`          | `Instant While Standing`                                 | ![ ](app/public/button/i^w^s.png)    |
| `iWR`         | `iWR`          | `Instant While Running`                                  | ![ ](app/public/button/i^w^r.png)    |
| `Micro Dash`  | `mdash`        | `Micro Dash`                                             | ![ ](app/public/button/mdash.png)    |
| `Neutral (☆)` | `n`            | `Neutral (☆)`                                            | ![ ](app/public/button/n.png)        |
| `During Rage` | `rage`         | `During Rage`                                            | ![ ](app/public/button/rage.png)     |
| `~`           | `~`            | `Followed by, immediately`                               | ![ ](app/public/button/~.png)        |
| `:`           | `:`            | `Followed by, tight input window`                        | ![ ](app/public/button/'colon'.png)  |
| `<`           | `<`            | `Followed by, with delayed input`                        | ![ ](app/public/button/'delay1'.png) |
| `>`           | `>`            | `Followed by, with delayed input`                        | ![ ](app/public/button/'delay2'.png) |
| `*`           | `*`            | `Held input`                                             | ![ ](app/public/button/'hold'.png)   |
| `►`           | ` `            | `Next`                                                   | ![ ](app/public/button/'next'.png)   |
| `[`           | `[`            | `Optional start`                                         | ![ ](app/public/button/[.png)        |
| `]`           | `]`            | `Optional end`                                           | ![ ](app/public/button/].png)        |

| Raw notation  | How to request        | Description                                   |
| :------------ | :-------------------- | :-------------------------------------------- |
| `qcf`         | `qcf`                 | `Same as d,df,f`                              |
| `qcb`         | `qcb`                 | `Same as d,db,b`                              |
| `hcf`         | `hcf`                 | `Same as b,db,d,df,f`                         |
| `hcb`         | `hcb`                 | `Same as f,df,d,db,b`                         |
| `dp`          | `dp`                  | `Same as f,d,df`                              |
| `RA`          | `RA`                  | `Same as R`                                   |
| `ewgf`        | `ewgf`                | `Same as f,n,d,df,2`                          |
| `EWGF`        | `EWGF`                | `Same as f,n,d,df,2`                          |
| `HB`          | `HB`                  | `Same as 2+3,H`                               |
| `HS`          | `HS`                  | `Same as H,2+3`                               |
| `name_stance` | `stance(name_stance)` | `For using stance, use 'stance(name_stance)'` |
| `STB`         | `stance(STB)`         | `e.g for using stance'`                       |

#### Find moveset

```json
  POST /findmove
```

| Parameter        | Type     | Description                  |
| :--------------- | :------- | :--------------------------- |
| `character_name` | `string` | \*Character Name of Tekken 8 |
| `name_move`      | `string` | Name move to find            |
| `notation`       | `string` | Notation to find             |

#### Get moveset

```json
  POST /movetable
```

| Parameter        | Type     | Description                  |
| :--------------- | :------- | :--------------------------- |
| `character_name` | `string` | \*Character Name of Tekken 8 |

## Usage/Examples

#### Notation Maker:

```json
POST /notation
{
    "character_name": "lee",
    "notation": "b,B+4 dash b,3,3 f,4:1 b,1:1+2"
}
```

Output will be:
![Notation Maker Example](app/public/example/response.png)

#### Get movetable:

```http
POST /movetable
{
    "character_name": "kazuya"
}
```

Output will be:

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
    }
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

```http
POST /findmove
{
    "character_name": "claudio",
    "name_move": "jab"
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

Access server

```bash
  http://127.0.0.1:8000
```

## Run In Docker

Start the server

```bash
  docker pull dmmrs/tekken8-api:v1.0.2
```

Run the server

```bash
  docker run -d -p 8000:8000 dmmrs/tekken8-api:v1.0.2
```

Access server

```bash
  http://127.0.0.1:8000
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
