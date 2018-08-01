import React from 'react';

const genderOptions = [
    {key: 'male', text: 'Male', value: 'Male'},
    {key: 'female', text: 'Female', value: 'Female'},
];

class BirthSearchForm extends React.Component{
    render(){
        return(
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>a
                            <Form.Input label="First Name"
                                        name="firstName"
                                        placeholder="First Name"
                                        onChange={this.handleChange}
                                        value={this.state.firstName}
                            />
                            <Form.Input label="Middle Name"
                                        name="middleName"
                                        placeholder="Middle Name"
                                        onChange={this.handleChange}
                                        value={this.state.middleName}
                            />
                            <Form.Input label="Last Name"
                                        name="lastName"
                                        placeholder="Last Name"
                                        onChange={this.handleChange}
                                        value={this.state.lastName}
                            />
                        </Form.Group>
                        <Form.Input label="Birth Place"
                                    name="birthPlace"
                                    placeholder="BirthPlace"
                                    onChange={this.handleChange}
                                    value={this.state.birthPlace}
                        />
                        <Form.Select label="Gender"
                                     required
                                     name="gender"
                                     placeholder="Gender"
                                     options={genderOptions}
                                     onChange={(e, {value}) => {
                                         this.setState({gender: value});
                                         this.props.callBack("gender", value);
                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Mother Name"
                                    name="motherName"
                                    placeholder="Mother Name"
                                    onChange={this.handleChange}
                                    value={this.state.motherName}
                        />
                        <Form.Input label="Father Name"
                                    name="fatherName"
                                    placeholder="Father Name"
                                    onChange={this.handleChange}
                                    value={this.state.fatherName}
                        />
                        {VitalRecordForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}
export default BirthSearchForm;