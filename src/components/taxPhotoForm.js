import React from 'react';

class TaxPhotoForm extends React.Component {
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group inline>
                            <label>Collection</label>
                            <Form.Radio
                                name="collection"
                                label='1940s'
                                checked={this.state.collection === "1940s"}
                                onChange={(e, {}) => {
                                    this.setState({collection: "1940s"})
                                    this.props.callBack("collection", "1940s")
                                }}

                            />
                            <Form.Radio
                                name="collection"
                                label='1980s'
                                checked={this.state.collection === "1980s"}
                                onChange={(e, {}) => {
                                    this.setState({collection: "1980s"})
                                    this.props.callBack("collection", "1980s")
                                }}
                            />
                            <Form.Radio
                                name="collection"
                                label='Both'
                                checked={this.state.collection === "Both"}
                                onChange={(e, {}) => {
                                    this.setState({collection: "Both"})
                                    this.props.callBack("collection", "Both")
                                }}
                            />
                        </Form.Group>

                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    onChange={this.handleChange}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={this.handleChange}
                                    value={this.state.lot}
                        />
                        <Form.Input label="Roll"
                                    name="roll"
                                    placeholder="Roll#"
                                    onChange={this.handleChange}
                                    value={this.state.roll}
                        />
                        <Form.Group inline>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '"8 x 10" Print'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: "8x10"})
                                    this.props.callBack("printSize", "8x10")
                                }}

                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '"11 x 14" Print'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: "11x14"})
                                    this.props.callBack("printSize", "11x14")
                                }}
                            />
                        </Form.Group>
                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value);

                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={this.handleChange}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={this.handleChange}
                                    value={this.state.street}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail == false) ?
                                               this.props.callBack("mail", true) &&
                                               this.setState({mail: true}) :
                                               this.setState({mail: false}) &&
                                               this.props.callBack("mail", false);
                                       }}
                                       value={this.state.mail}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={this.handleChange}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={this.handleChange}
                                    value={this.state.contactNum}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>

    )
}
}
export default TaxPhotoForm;