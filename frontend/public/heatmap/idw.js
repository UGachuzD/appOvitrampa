const colors = [
    "#0f99dd", "#35bbdd", "#68dca7", "#e3f46c", "#fcfd61", "#fecf4f", "#fea43d", "#fa4815", '#FF2400'
];

//Funcion de interpolacion espacial IDW
function IDW(centro, puntos) {
    let exp = 2;
    let d = 0;
    let s1 = 0 // new Array();
    let s2 = 0 // new Array();
    for (let i = 0; i < puntos.length; i++) {
        d = Math.sqrt(Math.pow(parseFloat(puntos[i].longitud) - centro[1], 2) + Math.pow(parseFloat(puntos[i].latitud) - centro[0], 2));
        s1 += puntos[i].cantidad_huevos / Math.pow(d, exp);
        s2 += 1 / Math.pow(d, exp);
    }
    return s1 / s2
}
function getC(v, maximo) {
    var z = v / maximo
    if (z > maximo) {
        return colors[colors.length - 1];
    } else if (z <= 0) {
        return colors[0];
    }
    if (typeof (z) === "number") {
        return colors[Math.floor((colors.length - 1) * z)];
    }
    else {
        return colors[0];
    }
}

///Funcion que crea una imagen de una superficie interpolada usando idw
function crearSuperficieInterpolada(numCuadrosX, numCuadrosY, zi) {

    const canva = document.getElementById('canva');
    const ctx = canva.getContext('2d');
    const widthCanva = canva.width;
    const heightCanva = canva.height;

    // Borrar el contenido previo del canvas
    ctx.clearRect(0, 0, canva.width, canva.height);

    const tamCuadroX = widthCanva / numCuadrosX;
    const tamCuadroY = heightCanva / numCuadrosY;

    let j = numCuadrosY - 1;
    let w = 0;
    let e = 0.1
    for (let i = 0; i < numCuadrosX; i++) {
        for (let k = 0; k < numCuadrosY; k++) {
            if (zi[w]) {
                ctx.fillStyle = getC(zi[w], 84);
                ctx.fillRect(i * tamCuadroX - e, j * tamCuadroY - e, tamCuadroX + e, tamCuadroY + e);
            }
            w++;
            j--;
        }
        j = numCuadrosY - 1;
    }
    return canva.toDataURL("image/png")
}