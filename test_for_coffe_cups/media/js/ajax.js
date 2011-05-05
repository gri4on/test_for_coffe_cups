  function run() {
   function enableDatePicker(){
       $("#id_date_birth").datepicker({ 
          changeMonth: true,
          changeYear : true,
          dateFormat : 'yy-mm-dd'
       });
   }

   // Create datePicker
   enableDatePicker();
 
  // prepare Options Object 
  var options = { 
      target:     '#edit_form',
      beforeSubmit: onAjaxRun, // handler that runs before submit
      success: onAjaxFinish
  };

   function onAjaxRun(){
    var change_form = $($("#change_form")[0]);
    // Disable form for User
    change_form.find('input').each(function(index, value) {value.disabled=true;});
    change_form.find('textarea').each(function(index, value) {value.disabled=true;});

    // Show loader image
    $("#loader").css('display', 'block').animate({opacity:1}, 'fast');
   }

  function onAjaxFinish() {
    var change_form = $($("#change_form")[0]);
    //Hide loader image
    $("#loader").css({'display': 'none', 'opacity':0});
    
    // Enable editable tags: input and textarea
    change_form.find('input').each(function(index, value) {value.disabled=false;});
    change_form.find('textarea').each(function(index, value) {value.disabled=false;});
    // create new datapicker
    enableDatePicker();
    // create new jquery form
    $("#change_form").ajaxForm(options);
  }
   
  // Create ajaxForm form jquery.form plugin
  $("#change_form").ajaxForm(options);
 
  };
