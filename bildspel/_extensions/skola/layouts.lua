-- A slide layout is a class on the slide heading, for example
-- "## Rubrik {.cover}". The look of each layout lives in skola.scss.
-- The background has to be set here, because reveal.js paints it
-- outside the slide element where the theme CSS cannot reach it.
local backgrounds = {
  cover = "#1D2433",
  closing = "#1D2433",
  tinted = "#F1ECE0",
}

function Header(el)
  if el.level ~= 2 then
    return nil
  end
  for layout, color in pairs(backgrounds) do
    if el.classes:includes(layout) and not el.attributes["background-color"] then
      el.attributes["background-color"] = color
    end
  end
  return el
end
