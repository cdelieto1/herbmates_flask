function StatusButton(props) {

  return (
    <button className={props.className} onClick={props.onClick}>
      {props.text}
    </button>
  );
}

class ListingCard extends React.Component {
  render() {
  return (
    <div className={[2, 3].includes(this.props.status) ? 'card pending' : 'card'}>
      <div className="bootcards-list col-sm-10">
      <p>Herb: <b>{this.props.herb_name}</b></p>
      <p>This herb is currently owned by: <b>{this.props.fname}</b> </p>
      <p>Quantity: <b>{this.props.herb_qty}</b></p>
      <img src={this.props.img_url}></img>
      <p>Additional info for this bundle: {this.props.pickup_instructions}</p>
      <p>This herb will expire on: {this.props.exp_date}</p>

      {this.props.pickup_instructions && <p class="notification"><span class="badge badge-primary">{ this.props.pickup_instructions }</span></p>}

      {this.props.button}
    </div>
  </div>
  );
  }
}

class InventoryContainer extends React.Component {
  constructor() {
    super();
    //this.updateInventoryStatus = this.updateInventoryStatus.bind(this);

    this.state = { data: [] };  // Set initial value
    this.updateInventory = this.updateInventory.bind(this);
  }

  updateInventory(response) {
    const inventory = response.data;
    this.setState({ inventory: inventory });
  }

  getInventoryData() {
    $.get('/get-inventory', this.updateInventory);
  }

  componentDidMount() {
    this.getInventoryData();
  }

  updateInventoryStatus(inTask, inInventoryId, inPickupInstr) {
    // port js in other homepage post over here???
    console.log('clicked button - firing updateInventoryStatus()');
    console.log(inTask, inInventoryId, inPickupInstr);
  }

  confirmPickup(inInventoryId) {

    Swal.fire({
      title: 'Are you sure?',
      text: "This herb will be reserved and the owner will be notified!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, request pickup!'
    }).then((result) => {
      if (result.value) {
        this.updateInventoryStatus('pickup', inInventoryId, '');
      }
    })

  }

  confirmDeletion(inInventoryId) {

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
        this.updateInventoryStatus('delete', inInventoryId, '');
      }
    })

  }

  pickupReady(inInventoryId) { 

    Swal.fire({
      title: 'Enter your pickup instructions',
      input: 'text',
      inputValue: '',
      showCancelButton: true,
      inputValidator: (value) => {
        if (!value) {
          return 'You need to write something!'
        } else {
          this.updateInventoryStatus('ready', inInventoryId, value);
        }
      }
    })
  }

  render() {
    console.log('Cassies testing...');
    //console.log(this.state.inventory);
    const listingCards = [];

    if (this.state.inventory != undefined) {
      for (const currentListing of this.state.inventory) {

       let button;
       if ( currentListing.status == 1 && currentListing.user_id != currentListing.session_user_id ) {
          button = <StatusButton className="btn btn-md btn-primary" text="Request this herb" onClick={() => this.confirmPickup(currentListing.inventory_id)} />
       } else if ( currentListing.status == 1 && currentListing.user_id == currentListing.session_user_id ) {
          button = <StatusButton className="btn btn-md btn-danger" text="Delete this herb" onClick={() => this.confirmDeletion(currentListing.inventory_id)} />
       } else if ( currentListing.status == 2 && currentListing.user_id == currentListing.session_user_id ) {
          button = <StatusButton className="btn btn-md btn-success" text="Prepare Pickup" onClick={() => this.pickupReady(currentListing.inventory_id)} />
       }

        listingCards.push(
          <ListingCard
            key={currentListing.inventory_id}
            status={currentListing.status}
            fname={currentListing.fname}
            exp_date={currentListing.exp_date}
            herb_qty={currentListing.herb_qty}
            pickup_instructions={currentListing.pickup_instructions}
            herb_name={currentListing.herb_name}
            img_url={currentListing.img_url}
            button={button}
          />
        );
      }
    }

    return (
      <div className="card-content">{listingCards}
      </div>
    );
  }
}


ReactDOM.render(<InventoryContainer />, document.getElementById('herb-list'));
