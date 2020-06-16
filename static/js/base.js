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

       if (response == 'success') {
        // add sweet alerts with success
        alert("Status updated successfully!")
        location.reload();
       } else {
        alert("Something went wrong!");
       }
     }
 });

}

function doPickupReady(inInventoryId) {


  // sweet alerts:
  // updateStatus('ready', inInventoryId, textFromSweetalerts);

}

// $.post(url, [data,] successFunction). 
// Use this if you want to make a POST call and don’t want to
// load the response to some container DOM.