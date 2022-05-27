

function marcar_nro(campo) {
    div = document.getElementById(campo);
    if (div.classList.contains("btn_rojo")) {document.getElementById(campo).classList.remove("btn_rojo");} else {document.getElementById(campo).classList.add("btn_rojo");}

}

function mostrar_carton(indice1) {
    var campo1 = "contentgenrut"+indice1;
    var item = document.getElementById(campo1);
    //alert(item);
    var hasClase2 = item.classList.contains( 'hidden' );
    if (hasClase2) {
        document.getElementById(campo1).classList.remove("hidden");
        } else document.getElementById(campo1).classList.add("hidden");

 
}
