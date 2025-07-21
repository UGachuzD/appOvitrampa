// bbox = [minX, minY, maxX, maxY]
function expandBBox(bbox, factor = 1.2) {
  const [minX, minY, maxX, maxY] = bbox;

  const width = maxX - minX;
  const height = maxY - minY;

  const centerX = (minX + maxX) / 2;
  const centerY = (minY + maxY) / 2;

  const newWidth = width * factor;
  const newHeight = height * factor;

  const newMinX = centerX - newWidth / 2;
  const newMaxX = centerX + newWidth / 2;
  const newMinY = centerY - newHeight / 2;
  const newMaxY = centerY + newHeight / 2;

  return [newMinX, newMinY, newMaxX, newMaxY];
}
