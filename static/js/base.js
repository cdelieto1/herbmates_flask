//The functions to manuever between an herb owner and an herb requester using AJAX and alerts. 

const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 2000,
  timerProgressBar: true,
  onOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
})

function updateStatus(inTask, inInventoryId, inPickupInstr) {

   jQuery.ajax({
     type: "POST",
     url: "/update_inventory_status",
     data: {task: inTask,
            inventory_id: inInventoryId,
            pickup_instructions: inPickupInstr
            },
     cache: false, 
     success: function(response)
     {
       console.log("Request sent to update status");
       console.log(response);

// remove console.log before final commit

       if (response == 'success') {

          msg = 'Listing successfully updated!'
          if ( inTask == 'request' ) {
            msg = "Herb requested successfully! You'll get notified once its ready for pickup.";
          } else if ( inTask == 'ready' ) {
            msg = "You will be notified once the herb has been picked up.";
          } else if ( inTask == 'complete') {
            msg = "All set! Enjoy your herb!"
          } else if ( inTask == 'delete' ) {
            msg = "Herb has been successfully deleted!";
          } else if ( inTask == 'cancel' ) {
            msg = "Pickup request successfully cancelled!"
          }

          Toast.fire({
            icon: 'success',
            title: msg
          }).then((result) => {
            location.reload();
          })

       } else {
          Swal.fire(
            'Try again',
            'Something went wrong.',
            'error'
          )

       }
     }
 });

}

function confirmDeletion(inInventoryId) {

  Swal.fire({
    title: 'Are you sure?',
    text: "This herb will be deleted permanently!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!'
  }).then((result) => {
    if (result.value) {
      updateStatus('delete', inInventoryId, '');
    }
  })

}

function confirmPickup(inInventoryId) {

  Swal.fire({
    title: 'Are you sure?',
    text: "The owner will be notified and you'll receive a SMS once its ready!",
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#28a745',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, request pickup!'
  }).then((result) => {
    if (result.value) {
      updateStatus('pickup', inInventoryId, '');
    }
  })

}

function pickupReady(inInventoryId) { 


  Swal.fire({
    title: 'Enter your pickup instructions',
    input: 'text',
    inputValue: '',
    showCancelButton: true,
    inputValidator: (value) => {
      if (!value) {
        return 'You need to write something!'
      } else {
        updateStatus('ready', inInventoryId, value);
      }
    }
  })
  

}
