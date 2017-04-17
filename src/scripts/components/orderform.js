/**
 * Created by sinsang on 4/17/17.
 */

export default class OrderForm extends React.Component{
    setDate () {
        // sets the state of the today variable to today's date
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        if (dd < 10) {
            dd = '0' + dd
        }
        if (mm < 10) {
            mm = '0' + mm
        }
        today = mm + '/' + dd + '/' + yyyy;
        this.setState({
            today: today
        });
    }
    
    findOrder (event) {
        // when 'Apply' button is pressed, an order object is created and passed to the filterOrder(order) function
        event.preventDefault();
        debugger;
        var order = {
            orderNumber: this.refs.orderNumber.value,
            subOrderNumber: this.refs.subOrderNumber.value,
            orderType: this.refs.orderType.value,
            billingName: this.refs.billingName.value,
            dateReceivedStart: this.refs.dateReceivedStart.value,
            dateReceivedEnd: this.refs.dateReceivedEnd.value
        };
        this.props.orderFilters.push(order);
        this.props.filterOrder(order)
    }
    
    componentWillMount () {
        // calls setDate() function on load of component
        this.setDate();
    }
    
    render() {
        return (
            <form className='apply-order' ref='orderForm' onSubmit={this.findOrder}>
                <input
                    data-bind='value: orderNumber'
                    type='text'
                    ref='orderNumber'
                    id='order-number'
                    placeholder='Order Number'/>
                <input
                    data-bind='value: subOrderNumber'
                    type='text'
                    ref='subOrderNumber'
                    id='suborder-number'
                    placeholder='Suborder Number'/>
                <select data-bind='value: orderType' ref='orderType' id='ordertype' defaultValue='Order Type'>
                    <option disabled>
                        Order Type
                    </option>
                    <option value='All'>
                        All
                    </option>
                    <option value='vitalrecords'>
                        --Vital Records--
                    </option>
                    <option value='Birth Search'>
                        Birth Search
                    </option>
                    <option value='Marriage Search'>
                        Marriage Search
                    </option>
                    <option value='Death Search'>
                        Death Search
                    </option>
                    <option value='Birth Cert'>
                        Birth Certificate
                    </option>
                    <option value='Marriage Cert'>
                        Marriage Certificate
                    </option>
                    <option value='Death Cert'>
                        Death Certificate
                    </option>
                    <option value='photos'>
                        --Photos--
                    </option>
                    <option value='Property Card'>
                        Property Card
                    </option>
                    <option value='Photo Tax'>
                        Photo Tax
                    </option>
                    <option value='Photo Gallery'>
                        Photo Gallery
                    </option>
                    <option disabled value='other'>
                        --Other--
                    </option>
                    <option value='multipleitems'>
                        Multiple Items In Cart
                    </option>
                    <option value='vitalrecordsphotos'>
                        Vital Records and Photos In Cart
                    </option>
                </select>
                <input
                    data-bind='value: billingName'
                    type='text'
                    ref='billingName'
                    id='billingname'
                    placeholder='Billing Name'/>
                <input
                    data-bind='value: dateReceivedStart'
                    type='text'
                    ref='dateReceivedStart'
                    placeholder='Date Received - Start'
                    id='date-received-start'
                    defaultValue={this.state.today}/>
                <input
                    data-bind='value: dateReceivedEnd'
                    type='text'
                    ref='dateReceivedEnd'
                    placeholder='Date Received - End'
                    id='date-received-end'/>
                <button type='reset'>
                    Clear
                </button>
                <button data-bind='click: findOrder' type='submit' name='submit' value='FindOrder'>
                    Apply
                </button>
                <br/>
            </form>
        )
    }
}

