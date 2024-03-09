# Фласк продавница

Ово је симулације електронске продавнице за одређену врсту производа. Направљена је базична конструкција апликације, чија је целокупна архитектура још комплекснија од ове, али ово је добра основа за наставак развоја апликације, што подразумева имплементацију нових функционалности, интеграцију спољашних сервиса (плаћање на пример), писање тестова за проверу исправности рада функција, као и тестова за интеграцију и симулацију понашања крајњег корисника.

Структура кода прати стандарде који подразумевају јасан и интуитиван код, организован у модуларним целинама ради лакшег разумевањај, одржавања, дебаговања, побољшања и тестирања.

Структура апликације је таква да су организовани ентитети по директоријумима, којима логички припадају, следећи MVC шаблон за развој апликације. Коришћено је виртуално окружење, како нне би било евентуалних конфликта између библиотека које се користе у виртуелном окружењу и истим библиотекама на нивоу оперативног система.

База је SQLite3, која иде у пакету са Фласк фрејмворком. У директоријуму `database` је SQL скрипта, којом може да се иницира база апликације. Мада приликом првог покретања апликације, апликација креира базу са неким основним подацима, како би мого да се презентује рад апликације. Коришћене су везе између табела један према један, један према више и више према више. Такође, свака табела има и примарни кључ, који је уједно и индекс табеле.

