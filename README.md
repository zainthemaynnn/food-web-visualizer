# Food Web
this was a little assignment I made for a teacher that a grade 9 ontario science class had to complete. they had to edit the python file in order to create a food web given to them.

uses `QtGraphics` of `PyQt6`.

## installation
```shell
pip install poetry
poetry install
py src/main.py
```

## usage
edit `define_organisms` under `src/main.py`. example:

```py
def define_organisms() -> list[Organism]:
    fox = Organism(
        "Fox",                              # name
        Diet.Omnivore,                      # diet
        "https://fox-images.com/fox.png"    # image
    )

    rabbit = Organism(
        "Rabbit",
        Diet.Herbivore,
        "C://Downloads/cute/rabbit.png"
    )

    # create an arrow from the fox to the rabbit
    fox.consume(rabbit)

    # return every organism for rendering
    return [fox, rabbit]
```
