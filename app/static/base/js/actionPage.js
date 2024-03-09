function validSelect(){
    if( $('input[name="checkbox1"]:checked').length == 1 ){
    	return $('input[name="checkbox1"]:checked').val();
    }
    else { 
    	/*if( $.isNumeric($('#idActTable').val()) == true ){
    		return $('#idActTable').val();
    	}*/
    	if($('#idActTable').val() != ''){
    		return $('#idActTable').val();
    	}
    	else {
    		jsAlertBox('info','Selecione!','Selecione 1 (um) item da Listagem!');
			return false;
    	}
    }
}


function actionPage(){
	var id = validSelect();
	if (id != false){
		var href=window.location+id
		location.href=href;
	}
}

function actionDel(id){
	var idMov = validSelect();
	if( idMov  == false){
		return false;
	}else{
		deletaReg(idMov);
    }
}

function CKupdate(){
	if (typeof CKEDITOR !== 'undefined') {
        for (instance in CKEDITOR.instances)
            CKEDITOR.instances[instance].updateElement();
    }
}

function jsBoxCustom(title,msg,link,id){
	
	 if( $.isNumeric($('#idActTable').val()) == false ){
		 jsAlertBox('info','Selecione!','Selecione 1 (um) item da Listagem!');
		return false;
	  }else
		  
		var id = $('#idActTable').val();  
	 	Lobibox.confirm( {
		  title: title,
		  icon: true,
		  msg: 'Realmente deseja excluir?',
		     buttons: {
		         load: {
		         'class': 'btn btn-success',
		          text: 'Ok'
		         },
		         close: {
		          'class': 'btn btn-info',
		             text: 'Cancelar',
		             closeOnClick: true
		         }
		     },
		     callback: function(lobibox, type){
		      if (type === 'load'){
		       window.location = link+'?act=del&id='+id;
		      }
		      if (type === 'close'){
		       transfSol(id);
		      }
		     }
		 });
}


function jsBoxCustomGeneric(title,msg,link,id){
	
	if(msg){
		msg = msg;
	}else{
		msg = 'Realmente deseja excluir?';
	}
	
	
 	Lobibox.confirm( {
	  title: title,
	  icon: true,
	  msg: msg,
	     buttons: {
	         load: {
	         'class': 'btn btn-success',
	          text: 'Ok'
	         },
	         close: {
	          'class': 'btn btn-info',
	             text: 'Cancelar',
	             closeOnClick: true
	         }
	     },
	     callback: function(lobibox, type){
	      if (type === 'load'){
	       window.location = link+'&id='+id;
	      }
	      if (type === 'close'){
	    	  lobibox.hide();
	    	  //transfSol(id);
	      }
	     }
	 });
}

function jsBoxCustomModalDelete(title,msg,link,id,modal_link,modal_title){
 	Lobibox.confirm( {
	  title: title,
	  icon: true,
	  msg: 'Realmente deseja excluir?',
	     buttons: {
	         load: {
	         'class': 'btn btn-success',
	          text: 'Ok'
	         },
	         close: {
	          'class': 'btn btn-info',
	             text: 'Cancelar',
	             closeOnClick: true
	         }
	     },
	     callback: function(lobibox, type){
	    	 if (type === 'load'){
	    	  
	    	  var array = id.split(",");
	    	  var item = {}
	    	  item ["id"] = array[0];
	    	  $.ajax({
	    		  type: 'post',
	    		  url: link,
	    		  data: item,
	    		  success: function(data){
	    			  if( data == 1 ){
	    				  jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
	    				  //$('div[name=' + name + ']').modal('hide');
	    				  return true;
	    			  }else{
	    				  jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
	    				  return false;
	    			  }
	    		  }
	    	  });	
	    	  lobibox.hide();
	    	  voltarMdlVisDel(array[1]);
	    	  return true;
	    	  
	    	  function voltarMdlVisDel(cod){
				setTimeout(function(){
				 	$.ajax({
				  		type: 'get',
				  		url: modal_link+'id='+cod,
				  		data: {'id':cod},
				  		success: function(response) {
				  			$('.panel-heading h4').find('b').text(modal_title);
				  			$('.modal-body div').html(response);
				  		},
				  	async: true
				  	});
				},2000);
	    	  }
	    	  
	    	 }
	    	 
	    	 if (type === 'close'){
	    		 //console.log(id);
	    		 try{
	    			 transfSol(id);
	    		 }catch(error){console.log(error)}
	    		 lobibox.hide();
	    	 }
	     }
	 });
}


function jsBoxCustomModalDeleteEndExec(title,msg,link,id,execFunction,modalHidden){
 	Lobibox.confirm( {
	  title: title,
	  icon: true,
	  msg: 'Realmente deseja excluir?',
	     buttons: {
	         load: {
	         'class': 'btn btn-success',
	          text: 'Ok'
	         },
	         close: {
	          'class': 'btn btn-info',
	             text: 'Cancelar',
	             closeOnClick: true
	         }
	     },
	     callback: function(lobibox, type){
	    	 if (type === 'load'){
	    	  
	    	  var array = id.split(",");
	    	  var item = {}
	    	  item ["id"] = array[0];
	    	  $.ajax({
	    		  type: 'post',
	    		  url: link,
	    		  data: item,
	    		  success: function(data){
	    			  if( data == 1 ){
	    				  jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
	    				  
	    				  if(modalHidden){
	    					  $('div[name='+modalHidden+']').modal('hide');
	    				  }
	    				  return true;
	    				  
	    				  
	    			  }else{
	    				  jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
	    				  return false;
	    			  }
	    		  }
	    	  });	
	    	  lobibox.hide();
	    	  
	    	  
	    	  if(execFunction){
	    		  execOpenModal();
	    	  }
	    	  return true;
	    	 }
	    	 
	    	 if (type === 'close'){
	    		 //console.log(id);
	    		 try{
	    			 transfSol(id);
	    		 }catch(error){console.log(error)}
	    		 lobibox.hide();
	    	 }
	     }
	 });
}



function jsBoxCustomModalDeleteEndExecComId(title,msg,link,id,execFunction,modalHidden,modalOpen){
	
 	Lobibox.confirm( {
	  title: title,
	  icon: true,
	  msg: 'Realmente deseja excluir?',
	     buttons: {
	         load: {
	         'class': 'btn btn-success',
	          text: 'Ok'
	         },
	         close: {
	          'class': 'btn btn-info',
	             text: 'Cancelar',
	             closeOnClick: true
	         }
	     },
	     callback: function(lobibox, type){
	    	 if (type === 'load'){
	    	  
	    	  var array = id.split(",");
	    	  var item = {}
	    	  item["id"] = array[0];
	    	  $.ajax({
	    		  type: 'post',
	    		  url: link,
	    		  data: item,
	    		  success: function(data){
	    			  if( data == 1 ){
	    				  jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
	    				  
	    				  if(modalHidden){
	    					  $('div[name='+modalHidden+']').modal('hide');
	    				  }
	    				  return true;
	    				  
	    				  
	    			  }else{
	    				  jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
	    				  return false;
	    			  }
	    		  }
	    	  });	
	    	  lobibox.hide();
	    	  
	    	  
	    	  if(execFunction){
	    		  if(modalOpen){
	    			  
    			  	if(modalOpen == 'execOpenModalAnexos'){
			  			execOpenModalAnexos(array[1]);
	    		  	}
    			  	
    			  	if(modalOpen == 'execOpenModalFotos'){
			  			execOpenModalFotos(array[1]);
	    		  	}
	    			
	    		  }else{
    			  	execOpenModal(array[1]);
	    		  }
	    		  
	    	  }
	    	  return true;
	    	 }
	    	 
	    	 if (type === 'close'){
	    		 //console.log(id);
	    		 try{
	    			 transfSol(id);
	    		 }catch(error){console.log(error)}
	    		 lobibox.hide();
	    	 }
	     }
	 });
}

function createDataTableJS(url, tab, strip, buttons) {
    strip = jQuery.parseJSON(strip);
    $.ajax({
        async: false,
        "url": url + "?f=json",
		"contentType": 'application/json', // Aqui está o cabeçalho Content-Type: application/json"
        "processing": true,
        "serverSide": false,
        "success": function(json) {
            if (json.error) {
                $("#tableDiv").append('<div class="alert alert-danger margin-top-40"><b>Sem Dados para Mostrar!</b></div>');
            } else {
                var tableHeaders = "";
                var tColumns = [];
                $.each(json.columns, function(i, val) {
                    tableHeaders += "<th>" + val + "</th>";
                    tColumns.push({ "name": val });
                });
                $("#tableDiv").empty();
                $("#tableDiv").append('<table id="' + tab + '" class="table responsive table-condensed table-striped table-bordered table-hover table-responsive" cellspacing="0" width="100%"><thead><tr>' + tableHeaders + '</tr></thead></table>');

                var table = $('#' + tab).DataTable({
                    "language": { "url": "./base/classes/datatables/Portuguese-Brasil.json" },
                    "dom": 'Bfrtip',
                    "lengthChange": false,
                    "processing": true,
                    "serverSide": false,
                    "order": [
                        [0, "desc"]
                    ],
                    "info": true,
                    "select": { style: 'single' },
                    "deferRender": false,
                    "pageResize": true,
                    "filter": true,
                    "lengthMenu": [
                        [12, 50, 100, 250, 500, 1000],
                        ['12 linhas', '50 linhas', '100 linhas', '250 linhas', '500 linhas', '1000 linhas']
                    ],
                    "ajax": {
                        url: url + "?f=json",
                        type: "GET",
						contentType: 'application/json', // Aqui está o cabeçalho Content-Type: application/json
                        dataType: 'json',
                        error: function(res) {
                            if (res.status == 500) {
                                var erro = res.responseJSON;
                                jsAlertBox('error', 'Erro ao buscar registros.', erro.message + "<pre style='width: 482px;height: 200px;'>" + res.responseText + "</pre>");
                            } else {
                                jsMensageBox("warning", "normal", "Sem Registros", "Correspondente a Pesquisa: " + $(".dataTables_filter input").val(), "10000", 450);
                                $(".dataTables_filter input").val("");
                            }
                        }
                    },
                    "buttons": [
                        { extend: 'copy', text: '<u>C</u>opiar', key: { key: 'c', altKey: true } }, 'csv', 'excel', 'pdf', { extend: 'print', text: '<u>I</u>mprimir', key: { key: 'i', altKey: true } }, { extend: 'colvis', text: 'Coluna Visivel' }, { extend: 'pageLength', text: 'Registros', className: 'btn-danger' }
                    ],
                    "columns": tColumns,
                    "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
                        if (strip) {
                            $.each(strip.bg, function(key, value) {
                                if (aData[strip.col] == key) {
                                    $(nRow).addClass(value);
                                }
                            });
                            this.removeClass('table-striped');
                        }
                    },
                    "initComplete": function() {
                        if (buttons) {
                            $.each(buttons, function(i, val) {
                                table.button().add(i, {
                                    text: '<b>' + val.label + '</b>',
                                    action: function(e, dt, node, config) {
                                        setTimeout(val.link, 100);
                                    }
                                });
                            });
                        }
                    }
                });
                table
                    .on('select', function(e, dt, type, indexes) {
                        var rowData = table.rows(indexes).data().toArray();
                        $("#idActTable").val(rowData[0][0]);
                    })
                    .on('deselect', function(e, dt, type, indexes) {
                        $("#idActTable").val("");
                    });
            }
        }
    });
}



// function createDataTableJS(url, tab, strip, buttons) {
//     strip = jQuery.parseJSON(strip);
//     $.ajax({
//         async: true,
//         "url": url + "?draw=1&limit="+strip,
//         "processing": true,
//         "serverSide": true,
//         "success": function(json) {
//             if (json.error) {
//                 $("#tableDiv").append('<div class="alert alert-danger margin-top-40"><b>Sem Dados para Mostrar!</b></div>');
//             } else {
//                 var tableHeaders = "";
//                 var tColumns = [];
//                 $.each(json.columns, function(i, val) {
//                     tableHeaders += "<th>" + val + "</th>";
//                     tColumns.push({ "name": val });
//                 });
//                 $("#tableDiv").empty();
//                 $("#tableDiv").append('<table id="' + tab + '" class="table responsive table-condensed table-striped table-bordered table-hover table-responsive" cellspacing="0" width="100%"><thead><tr>' + tableHeaders + '</tr></thead></table>');

//                 var table = $('#' + tab).DataTable({
//                     "language": { "url": "./base/classes/datatables/Portuguese-Brasil.json" },
//                     "dom": 'Bfrtip',
//                     "lengthChange": false,
//                     "processing": true,
//                     "serverSide": true,
//                     "order": [
//                         [0, "desc"]
//                     ],
//                     "info": true,
//                     "select": { style: 'single' },
//                     "deferRender": false,
//                     "pageResize": true,
//                     "filter": true,
//                     "lengthMenu": [
//                         [12, 50, 100, 250, 500, 1000],
//                         ['12 linhas', '50 linhas', '100 linhas', '250 linhas', '500 linhas', '1000 linhas']
//                     ],
//                     "ajax": {
//                         url: url,
//                         type: "GET",
//                         dataType: 'json',
//                         error: function(res) {
//                             if (res.status == 500) {
//                                 var erro = res.responseJSON;
//                                 jsAlertBox('error', 'Erro ao buscar registros.', erro.message + "<pre style='width: 482px;height: 200px;'>" + res.responseText + "</pre>");
//                             } else {
//                                 jsMensageBox("warning", "normal", "Sem Registros", "Correspondente a Pesquisa: " + $(".dataTables_filter input").val(), "10000", 450);
//                                 $(".dataTables_filter input").val("");
//                             }
//                         }
//                     },
//                     "buttons": [
//                         { extend: 'copy', text: '<u>C</u>opiar', key: { key: 'c', altKey: true } }, 'csv', 'excel', 'pdf', { extend: 'print', text: '<u>I</u>mprimir', key: { key: 'i', altKey: true } }, { extend: 'colvis', text: 'Coluna Visivel' }, { extend: 'pageLength', text: 'Registros', className: 'btn-danger' }
//                     ],
//                     "columns": tColumns,
//                     "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
//                         if (strip) {
//                             $.each(strip.bg, function(key, value) {
//                                 if (aData[strip.col] == key) {
//                                     $(nRow).addClass(value);
//                                 }
//                             });
//                             this.removeClass('table-striped');
//                         }
//                     },
//                     "initComplete": function() {
//                         if (buttons) {
//                             $.each(buttons, function(i, val) {
//                                 table.button().add(i, {
//                                     text: '<b>' + val.label + '</b>',
//                                     action: function(e, dt, node, config) {
//                                         setTimeout(val.link, 100);
//                                     }
//                                 });
//                             });
//                         }
//                     }
//                 });
//                 table
//                     .on('select', function(e, dt, type, indexes) {
//                         var rowData = table.rows(indexes).data().toArray();
//                         $("#idActTable").val(rowData[0][0]);
//                     })
//                     .on('deselect', function(e, dt, type, indexes) {
//                         $("#idActTable").val("");
//                     });
//             }
//         }
//     });
// }





function openLink(url,data){
	if( data == true ){
		if( validSelect() == false ){
			return false;
		}
		var idMov = validSelect();
		console(idMov)
		var urlFinal = url+idMov+'/';
	}else{
		var urlFinal = url;
	}	
	window.open(urlFinal, '_blank');
}


function sysModalBoxJs(title, data, nome, tamanho, color, bclose, endpoint){
	
	
if( data == true ){
	if( validSelect() == false ){
		return false;
	}
	var idMov = validSelect();
	var urlFinal = window.location + idMov + endpoint
}else{
	var urlFinal = window.location;
}

if( tamanho != 'undefined' ){
	tamanho = tamanho;
}else{
	tamanho ='';
}

if( bclose === 'true' ){
	bclose = 'data-backdrop="static" data-keyboard="false"';
}else{
	bclose ='';
}

if(color != 'undefined'){
	color = 'panel-'+color;
}else{
	color = 'panel-default';
}

if( nome != 'undefined' ){
	var box = nome;
	nome = 'name="'+nome+'"';
}else{
	var box = Math.random();
}


var html = '<div class="modal fade" id="modalBox'+box+'" '+nome+' role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" '+bclose+'>';
	html+= '<div class="modal-dialog '+tamanho+'">';
			html+= '<div class="panel '+color+' modal-content">';
				html+= '<div class="panel-heading">';
				html+= '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
				html+= '<h4><b>'+title+'</b>  <em></em></h4></div>';
					html+= '<div class="row modal-body">';
					html+= '<div id="modalBoxDetalhe'+box+'"><div class=" text-center"><img src="images/Preloader_3.gif" width="64" height="64"><br> Carregando...</div>';
			html+= '</div></div></div></div></div>';
jQuery('#divModalBox').append( html );
$('#modalBox'+box).modal('show');
$('#modalBoxDetalhe'+box).load( urlFinal + "&embedded=true");
	$('#modalBox'+box).on('hidden.bs.modal', function (e) {
		onExitModal();
		$('#modalBox'+box).remove();
	});
}



function sysModalBoxJsOnExitModal(title, url, data, nome, tamanho, color, bclose){
	
	
	if( data == true ){
		if( validSelect() == false ){
			return false;
		}
		var idMov = validSelect();
		var urlFinal = url + '&id=' + idMov;
	}else{
		var urlFinal = url;
	}

	if( tamanho != 'undefined' ){
		tamanho = tamanho;
	}else{
		tamanho ='';
	}

	if( bclose === 'true' ){
		bclose = 'data-backdrop="static" data-keyboard="false"';
	}else{
		bclose ='';
	}

	if(color != 'undefined'){
		color = 'panel-'+color;
	}else{
		color = 'panel-default';
	}

	if( nome != 'undefined' ){
		var box = nome;
		nome = 'name="'+nome+'"';
	}else{
		var box = Math.random();
	}

	//var box = url.length;
	var onModalHide = function() {
	    $('#modalBox'+box).remove();
	};


	var arq = url.split('?');
	var html = '<div class="modal fade" id="modalBox'+box+'" '+nome+' role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" '+bclose+'>';
		html+= '<div class="modal-dialog '+tamanho+'">';
				html+= '<div class="panel '+color+' modal-content">';
					html+= '<div class="panel-heading">';
					html+= '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
					html+= '<h4><b>'+title+'</b>  <em></em></h4></div>';
						html+= '<div class="row modal-body">';
						html+= '<div id="modalBoxDetalhe'+box+'"><div class=" text-center"><img src="images/Preloader_3.gif" width="64" height="64"><br> Carregando...</div>';
				html+= '</div></div></div></div></div>';
	jQuery('#divModalBox').append( html );
	$('#modalBox'+box).modal('show');
	$('#modalBoxDetalhe'+box).load( urlFinal + "&embedded=true");
		$('#modalBox'+box).on('hidden.bs.modal', function (e) {
			
			onExitModal2();
			onExitModal();
			
			$('#modalBox'+box).remove();
		});
	}


function sysModalBox(title, url, width, height, data, alerta, nome, tamanho, color, bclose){
	
	//var params = url.split('?')[1] ? true : false;	
		
	if( data == true ){
		if( validSelect() == false ){
			return false;
		}
		var idMov =  validSelect();
		var urlFinal = url + '&id=' + idMov;
		//var urlFinal = url + (params?'&':'?')+'id=' + idMov;
	}else{
		var urlFinal = url;
	}
	if( alerta != 'undefined' ){
		alerta = 'alert alert-'+alerta;
	}
	if( nome != 'undefined' ){
		nome = 'name="'+nome+'"';
	}


	if( tamanho != 'undefined' ){
		tamanho = tamanho;
	}else{
		tamanho ='';
	}

	if( bclose === 'true' ){
		bclose = 'data-backdrop="static" data-keyboard="false"';
	}else{
		bclose ='';
	}

	if(color != 'undefined'){
		color = 'panel-'+color;
	}else{
		color = 'panel-default';
	}

	var html = '<div class="modal fade" id="modalBox" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" '+bclose+'>';
		html+= '<div class="modal-dialog '+tamanho+'">';
				html+= '<div class=" panel '+color+' modal-content">';
					html+= '<div class="panel-heading">';
					html+= '<button type="button" class="close close-modal-sysModalBoxJs" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
					html+= '<h4><b>'+title+'</b>  <em></em></h4></div>';
						html+= '<div class="row modal-body modal-body-frame" id="modalBoxDetalhe">';
						html+= '<div class="col-xs-12 text-center" id="loading"><br><br><img src="images/Preloader_3.gif" width="64" height="64"></div>';
						html+= '<iframe src="' + urlFinal + '&embedded=true" '+nome+' width="100%" height="'+height+'" style="border: none;" onload="jaCarregado()"></iframe>';
						//html+= '<div id="modalDetalhe"></div>';
				html+= '</div></div></div></div>';
	jQuery('#divModalBox').append( html );
	$('#modalBox').modal('show');
	//$('#modalBoxDetalhe').load( urlFinal + "&embedded=true");
		$('#modalBox').on('hidden.bs.modal', function (e) {
			//onExitModal();
			$('#modalBox').remove();
		});
	//console.log(urlFinal);	
	}


function sysModalBoxExport(title, url, width, height, data, alerta, nome, tamanho, color, bclose){
	
	//var params = url.split('?')[1] ? true : false;	
		
	if( data == true ){
		if( validSelect() == false ){
			return false;
		}
		var idMov =  validSelect();
		var urlFinal = url + '&id=' + idMov;
		//var urlFinal = url + (params?'&':'?')+'id=' + idMov;
	}else{
		var urlFinal = url;
	}
	if( alerta != 'undefined' ){
		alerta = 'alert alert-'+alerta;
	}
	if( nome != 'undefined' ){
		nome = 'name="'+nome+'"';
	}


	if( tamanho != 'undefined' ){
		tamanho = tamanho;
	}else{
		tamanho ='';
	}

	if( bclose === 'true' ){
		bclose = 'data-backdrop="static" data-keyboard="false"';
	}else{
		bclose ='';
	}

	if(color != 'undefined'){
		color = 'panel-'+color;
	}else{
		color = 'panel-default';
	}

	var html = '<div class="modal fade" id="modalBoxExport" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" '+bclose+'>';
		html+= '<div class="modal-dialog '+tamanho+'">';
				html+= '<div class=" panel '+color+' modal-content">';
					html+= '<div class="panel-heading">';
					html+= '<button type="button" class="close close-modal-sysModalBoxJs" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
					html+= '<h4><b>'+title+'</b>  <em></em></h4></div>';
						html+= '<div class="row modal-body modal-body-frame" id="modalBoxDetalhe">';
						html+= '<div class="col-xs-12 text-center" id="loading"><br><br><img src="images/Preloader_3.gif" width="64" height="64"></div>';
						html+= '<iframe src="' + urlFinal + '&embedded=true" '+nome+' width="100%" height="'+height+'" style="border: none;" onload="jaCarregado()"></iframe>';
						//html+= '<div id="modalDetalhe"></div>';
				html+= '</div></div></div></div>';
	jQuery('#divModalBox').append( html );
	$('#modalBox').modal('show');
	//$('#modalBoxDetalhe').load( urlFinal + "&embedded=true");
		$('#modalBox').on('hidden.bs.modal', function (e) {
			//onExitModal();
			$('#modalBox').remove();
		});
	//console.log(urlFinal);	
	}

function jaCarregado(){
	$("#loading").hide().delay( 800 );
}


function jsMensageBox(tipo,size,title,msg,delay,width){
// tipo = "error", "info", "success", "warning"
if (width != null) {
	widt = 'width: width,';
}else{
	widt = '';
}
	Lobibox.notify(tipo, {
		size: size,
		howClass: 'rollIn',
		hideClass: 'rollOut',
		title: title,
		delay: delay,
		icon: true,
		position: 'bottom left',
		msg: msg,
	});
}
 
function jsAlertBox(tipo,title,msg){
// tipo = "error", "info", "success", "warning"
	Lobibox.alert(tipo, {
		title: title,
		icon: true,
		msg: msg,
	});
} 

// Converte texto para Maiusculo
function convMaiusc(z){
	v = z.value.toUpperCase();
	z.value = v;
}


function validacaoGeneric(title,msg,pagina,acao){
	Lobibox.alert('error', {
		title: title,
		icon: true,
		msg: msg,
		 buttons: {
	         load: {
	         'class': 'btn btn-default',
	          text: 'Ok'
	         }
	        
	     },
	     callback: function(lobibox, type){
	    	 if (type === 'load'){
	    		 window.location = pagina+'?act='+acao;
	      }
	     }
	});	
}


function validaInfo(title,msg,pagina,acao){
	Lobibox.alert('info', {
		title: title,
		icon: true,
		msg: msg,
		 buttons: {
	         load: {
	         'class': 'btn btn-default',
	          text: 'Ok'
	         }
	        
	     }
	});	
}

/**	Função para salvar no banco com foto
function jqSaveModal2(form,url,name){
	
	var dados = new FormData(); 
	dados.append('file',$('#arquivo').prop('files')[0]); 
	dados.append('post',$('#' + form).serialize());
	$.ajax({
		type: 'post',
		url: url,
		data: dados,
		dataType: 'text',
        cache: true,
        contentType: false,
        processData: false,
		success: function(data){
			if( data == 1 ){
				jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
				$('div[name=' + name + ']').modal('hide');
				return true;
			}else{
				jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
				return false;
			}
		}
	});	
	return true;	
}*/


/**	Função para slvar no banco sem arquivo
function jqSaveModal(form,url,name){
	var dados = $('#' + form).serialize();
	$.ajax({
		type: 'post',
		url: url,
		data: dados,
		success: function(data){
			if( data == 1 ){
				jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
				$('div[name=' + name + ']').modal('hide');
				return true;
			}else{
				jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
				return false;
			}
		}
	});	
	return true;	
}*/


/**	Função para salvar no banco */
function jqSaveDados(url,name,dados){	
	/*console.log(dados);*/
	$.ajax({
		type: 'post',
		url: url,
		data: dados,
		success: function(data){
			if( data == 1 ){
				jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
				$('div[name=' + name + ']').modal('hide');
				return true;
			}else{
				jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
				return false;
			}
		}
	});	
	return true;	
}




/**	Função para salvar no banco */
function jqSaveModal(form,url,name,cod,optional,modalOpen,onExitModal){
	/*$.blockUI({
		message: "<h3 style='margin-top:10px;'><img src='./images/spinner.gif' /> Aguarde...</h3>", 
	}); 
	*/
	CKupdate();
	$('button[type=submit]', $('#' + form)).attr('disabled', 'disabled');
	var frm = document.getElementById(form);
	var file = $('#' + form+' input:file').prop('files');
	var dados = new FormData(frm); 
	if( file ){
		dados.append('file',file );
	}
	if(optional){
		var cod_optional;
		cod_optional = optional;
	}
	$.ajax({
		type: 'post',
		url: url,
		enctype: 'multipart/form-data',
		dataType: 'text',
        cache: false,
        contentType: false,
        processData: false,
		data: dados,
		success: function(data){
			if( data == 1 ){
				$.unblockUI();
				jsMensageBox('success','normal','Salvo com Sucesso','Movimentação salva com Sucesso!','9000',450);
				$('div[name=' + name + ']').modal('hide');
				
				if(modalOpen){
					$.blockUI({
						message: "<h3 style='margin-top:10px;'><img src='./images/spinner.gif' /> Carregando...</h3>", 
					}); 
					execOpenModal();
				}
				
				if(onExitModal){
					//alert('aki');
					//onExitModal2();
					 setTimeout(function(){
						 onExitModal5();
					 },1500);
					
				}

				if(cod && cod_optional){
					voltarMdlVis2(cod,cod_optional);
				}else if(cod){
					voltarMdlVis2(cod);
				}
				return true;
			}else{
				$.unblockUI();
				jsMensageBox('error','normal','Erro ao Salvar',data,'60000',450);
				if(cod && cod_optional){
					voltarMdlVis2(cod,cod_optional);
				}else if(cod){
					voltarMdlVis2(cod);
				}
				return false;
			}
		}
	});

	$('button[type=submit]','#'+ form).removeAttr("disabled");	
	return false;	
}


$( document ).on( "mousemove", function( event ) {
	  $( "#log" ).text( "pageX: " + event.pageX + ", pageY: " + event.pageY );
	});





/**
* Retona a diferença entre duas horas.
* Exemplo: 14:35 a 17:21 = 02:46
* Adaptada de http://stackoverflow.com/questions/2053057/doing-time-subtraction-with-jquery
*/
function diferencaHoras(horaInicial, horaFinal) {
	// Se a hora inicial é menor que a final, faça a diferença tranquilamente	
	if( isHoraInicialMenorHoraFinal(horaInicial, horaFinal)){
	 	aux = horaInicial;
		horaInicial = horaFinal;
		horaInicial = aux;	

		hIni = horaInicial.split(':');
		hFim = horaFinal.split(':');

		horasTotal = parseInt(hFim[0], 10) - parseInt(hIni[0], 10);
		minutosTotal = parseInt(hFim[1], 10) - parseInt(hIni[1], 10);
		segundosTotal = parseInt(hFim[2], 10) - parseInt(hIni[2], 10);
		
		if(segundosTotal < 0){
			segundosTotal += 60;
			minutosTotal -= 1;
		}
		if(minutosTotal < 0){
			minutosTotal += 60;
			horasTotal -= 1;
		}
		
		horaInicial = completaZeroEsquerda(horasTotal) + ":" + completaZeroEsquerda(minutosTotal) + ":" + completaZeroEsquerda(segundosTotal);
		return horaInicial;
	} 
	
	// Aqui fica a gosto de quem for programar: se forem iguais, vc pode assumir que 
	// o intervalo é 24h ou zero. Depende de vc! Eu escolhi assumir que é 24h
	else if(horaInicial == horaFinal)
	{
		return "24:00";
	}
	
	// Se a hora inicial é maior que a final, então vou assumir que o 
	// horário inicial é de um dia e o final é do dia seguinte
	else
	{
		horasQueFaltamPraMeiaNoite = diferencaHoras(horaInicial, "24:00"); // chamada recursiva, há há!
		totalHoras = somaHora(horasQueFaltamPraMeiaNoite, horaFinal);
		return totalHoras;
	}
}


/**
 * Verifica se a hora inicial é menor que a final.
 * Exemplo: 10:50 < 22:10 ? Retorna true.
 */
function isHoraInicialMenorHoraFinal(horaInicial, horaFinal){
	horaIni = horaInicial.split(':');
    horaFim = horaFinal.split(':');

	// Verifica as horas. Se forem diferentes, é só ver se a inicial 
	// é menor que a final.
	hIni = parseInt(horaIni[0], 10);
	hFim = parseInt(horaFim[0], 10);
	if(hIni != hFim)
		return hIni < hFim;
	
	// Se as horas são iguais, verifica os minutos então.
    mIni = parseInt(horaIni[1], 10);
	mFim = parseInt(horaFim[1], 10);
	if(mIni != mFim)
		return mIni < mFim;
}

/**
 * Completa um número menor que dez com um zero à esquerda.
 * Usado aqui para formatar as horas... Exemplo: 3:10 -> 03:10 , 10:5 -> 10:05
 */
function completaZeroEsquerda( numero ){
	return ( numero < 10 ? "0" + numero : numero);
}


/**
* Soma duas horas.
* Exemplo:  12:35 + 07:20 = 19:55.
*/
function somaHora(horaInicio, horaSomada) {
	
    horaIni = horaInicio.split(':');
    horaSom = horaSomada.split(':');

    horasTotal = parseInt(horaIni[0], 10) + parseInt(horaSom[0], 10);
	minutosTotal = parseInt(horaIni[1], 10) + parseInt(horaSom[1], 10);
	
    if(minutosTotal >= 60){
        minutosTotal -= 60;
        horasTotal += 1;
    }
	
    horaTotal = completaZeroEsquerda(horasTotal) + ":" + completaZeroEsquerda(minutosTotal);
    return horaTotal ;
}


function inativarCampos(ids){
	ids.forEach(function(id){
		var wrap = $("#"+id+"_area");
		wrap.hide();
		wrap.find(':input').attr('required',null);
	});
}

function ativarCampos(ids,required){
	ids.forEach(function(id){
		var wrap =  $("#"+id+"_area");
		wrap.show();
		if(required){
			wrap.find('#'+id+':not(.summernote)').attr('required','');
		}
	});
}


function carregaThemes(){
	var id_theme =  $('#theme').val();
	
	if(id_theme) {
		
		$.getJSON('funcoes/color.ajax.php',{
			    id: id_theme ,
				ajax: 'true',
		}, 
		function(j){
			
			$("#theme-color").css("background-color",j[0].nome);
			$("#theme-color").css("color","#ffffff");
			
			$.unblockUI();
		});
	} else {
		$("#theme-color").css("background-color","#fffffff");
		$("#theme-color").css("color","#000000");
	
		$.unblockUI();
	}
}


function copyToClipboard(value) {
	
	var tempInput = document.createElement("input");
    tempInput.style = "position: absolute; left: -1000px; top: -1000px";
    tempInput.value = value;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
	
    jsMensageBox('success','normal','Copiado!',':)','2000',450);
}

function validarCPF(strCpf) {

	var soma;
	var resto;
	soma = 0;
	if (strCpf == "00000000000") {
		return false;
	}
	
	for (i = 1; i <= 9; i++) {
		soma = soma + parseInt(strCpf.substring(i - 1, i)) * (11 - i);
	}
	
	resto = soma % 11;
	
	if (resto == 10 || resto == 11 || resto < 2) {
		resto = 0;
	} else {
		resto = 11 - resto;
	}
	
	if (resto != parseInt(strCpf.substring(9, 10))) {
		return false;
	}
	
	soma = 0;
	
	for (i = 1; i <= 10; i++) {
		soma = soma + parseInt(strCpf.substring(i - 1, i)) * (12 - i);
	}
	resto = soma % 11;
	
	if (resto == 10 || resto == 11 || resto < 2) {
		resto = 0;
	} else {
		resto = 11 - resto;
	}
	
	if (resto != parseInt(strCpf.substring(10, 11))) {
		return false;
	}
	
	return true;
	}