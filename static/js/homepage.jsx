class ListingCard extends React.Component {
  render() {
  return (
    <div className="card">
      <div className="bootcards-list col-sm-10">
      <p>Herb: <b>{this.props.herb_name}</b></p>
      <p>This herb is currently owned by: <b>{this.props.fname}</b> </p>
      <p>Quantity: <b>{this.props.herb_qty}</b></p>
      <img src={this.props.img_url}></img>
      <p>Additional info for this bundle: {this.props.pickup_instructions}</p>
      <p>This herb will expire on: {this.props.exp_date}</p>
    </div>
  </div>
  );
  }
}

class InventoryContainer extends React.Component {
  constructor() {
    super();

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

  updateInventoryStatus() {
    // port jQuery post over here
  }

  render() {
    console.log('testing!...');
    console.log(this.state.inventory);
    const listingCards = [];

    if (this.state.inventory != undefined) {
      for (const currentListing of this.state.inventory) {

        /*let button;
        if (this.state.inventory.status) {
          button = <LogoutButton onClick={this.updateInventoryStatus} />;
        } else {
          button = <LoginButton onClick={this.updateInventoryStatus} />;
        }*/

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
          />
        );
      }
    }

    return (
      <div className="card-content">{listingCards}</div>
    );
  }
}


ReactDOM.render(<InventoryContainer />, document.getElementById('herb-list'));
