function fetchTransactions() {
    fetch('/get_transactions')
    .then(response => response.json())
    .then(data => {
        let textarea = document.getElementById('exampleFormControlTextarea1');
        textarea.value = data.join('\n');
    })
    .catch(error => {
        console.error('No hay transacciones en la base de datos:', error);
    });
}

document.getElementById('encryptButton').addEventListener('click', function(event) {
	    // Prevén el comportamiento predeterminado del botón (submit del formulario)
   event.preventDefault();
	//
	//         // Aquí puedes agregar cualquier lógica adicional que quieras ejecutar antes de consultar las transacciones
	//
	//             // Llama a la función que consulta las transacciones
   fetchTransactions();
	//
	//                     // Si deseas que, después de consultar las transacciones, se envíe el formulario, puedes hacerlo con el siguiente código:
	//                         // event.target.form.submit();
});



$(document).ready(function() {
    $("#encryptButton").click(function(e) {
	            // Muestra la barra de carga
	$("#loadingBar").show();
		    //                 
		    //                         // Si tu botón realiza una acción por defecto (por ejemplo, enviar un formulario),
		    //                                 // puedes querer detener esa acción para que la barra de carga se muestre correctamente.
		    //                                         // Si no es el caso, simplemente elimina la siguiente línea:
		    //                                                 // e.preventDefault();
	});
});


function updateLabel() {
    var input = document.getElementById('inputGroupFile02');
    var fileNameLabel = document.getElementById('file-name');
    if(input.files && input.files.length > 0) {
      fileNameLabel.textContent = input.files[0].name;
    } else {
      fileNameLabel.textContent = "Ningún archivo seleccionado";
    }
}


document.getElementById('downloadButton').addEventListener('click', function() {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/download_file', true);
	xhr.responseType = 'blob';
	xhr.onload = function() {
	    if (this.status === 200) {
		var blob = new Blob([this.response], {type: 'application/octet-stream'});
		var downloadUrl = URL.createObjectURL(blob);
		var a = document.createElement("a");
		a.href = downloadUrl;
		a.download = "archivo_descargado"; // El nombre que desees que tenga el archivo descargad
		document.body.appendChild(a);
		a.click();
		alert('Los ID de bloque correspondientes a las transacciones que incluyen los segmentos del archivo han sido recibidos y desencriptados con éxito. Por favor, consulte la carpeta de descargas para verificar el contenido del archivo.');
		a.remove();
	    }
	};
	xhr.send();
});
					    //                                                                 </script>
					    //



