const colours = ["blue", "green", "gold", "purple", "lightblue"] as const;
type ColourClass = (typeof colours)[number];

function generateColour(id: string) {
  let sum = 0;
  for (let i = 0; i < id.length; i++) {
    sum += id.charCodeAt(i) * id.charCodeAt(i > 1 ? i - 1 : i);
  }
  return sum % colours.length;
}

export function getColourClass(id: string): ColourClass {
  return colours[generateColour(id)];
}
