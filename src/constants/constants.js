export const CHUNK_SIZE = 150;

export const boroughOptions = [
    {key: 'bronx', text: 'Bronx', value: 'Bronx'},
    {key: 'brooklyn', text: 'Brooklyn', value: 'Brooklyn'},
    {key: 'manhattan', text: 'Manhattan', value: 'Manhattan'},
    {key: 'queens', text: 'Queens', value: 'Queens'},
    {key: 'statenisland', text: 'Staten Island', value: 'Staten Island'},
];

export const genderOptions = [
    {key: 'male', text: 'Male', value: 'Male'},
    {key: 'female', text: 'Female', value: 'Female'},
];

export const monthOptions = [
    {value: ''},
    {key: 'january', text: 'January', value: 'January'},
    {key: 'february', text: 'February', value: 'February'},
    {key: 'march', text: 'March', value: 'March'},
    {key: 'april', text: 'April', value: 'April'},
    {key: 'may', text: 'May', value: 'May'},
    {key: 'june', text: 'June', value: 'June'},
    {key: 'july', text: 'July', value: 'July'},
    {key: 'august', text: 'August', value: 'August'},
    {key: 'september', text: 'September', value: 'September'},
    {key: 'october', text: 'October', value: 'October'},
    {key: 'november', text: 'November', value: 'November'},
    {key: 'december', text: 'December', value: 'December'}
];

export const dayOptions = [
    {value: ''},
    {key: '1', text: '1', value: '1'},
    {key: '2', text: '2', value: '2'},
    {key: '3', text: '3', value: '3'},
    {key: '4', text: '4', value: '4'},
    {key: '5', text: '5', value: '5'},
    {key: '6', text: '6', value: '6'},
    {key: '7', text: '7', value: '7'},
    {key: '8', text: '8', value: '8'},
    {key: '9', text: '9', value: '9'},
    {key: '10', text: '10', value: '10'},
    {key: '11', text: '11', value: '11'},
    {key: '12', text: '12', value: '12'},
    {key: '13', text: '13', value: '13'},
    {key: '14', text: '14', value: '14'},
    {key: '15', text: '15', value: '15'},
    {key: '16', text: '16', value: '16'},
    {key: '17', text: '17', value: '17'},
    {key: '18', text: '18', value: '18'},
    {key: '19', text: '19', value: '19'},
    {key: '20', text: '20', value: '20'},
    {key: '21', text: '21', value: '21'},
    {key: '22', text: '22', value: '22'},
    {key: '23', text: '23', value: '23'},
    {key: '24', text: '24', value: '24'},
    {key: '25', text: '25', value: '25'},
    {key: '26', text: '26', value: '26'},
    {key: '27', text: '27', value: '27'},
    {key: '28', text: '28', value: '28'},
    {key: '29', text: '29', value: '29'},
    {key: '30', text: '30', value: '30'},
    {key: '31', text: '31', value: '31'}
];

export const createOrderTypeOptions = [
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
];

export const searchOrderTypeOptions = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'vitalrecords', text: '--Vital Records--', value: 'vital_records'},
    {key: 'birthsearch', text: 'Birth Search', value: 'Birth Search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'Marriage Search'},
    {key: 'deathsearch', text: 'Death Search', value: 'Death Search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'propertycard', text: 'Property Card', value: 'Property Card'},
    {key: 'hvr', text: 'HVR', value: 'HVR'},
    {key: 'noamends', text: 'No Amends', value: 'No Amends'},
    {key: 'ocme', text: 'OCME', value: 'OCME'},
    {key: 'photos', text: '--Photos--', value: 'photos'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
    {key: 'other', text: '--Other--', value: 'other', disabled: true},
    {key: 'multipleincart', text: 'Multiple Items In Cart', value: 'multiple_items'}
];

export const statusOptions = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'received', text: 'Received', value: 'Received'},
    {key: 'microfilm', text: 'Microfilm', value: 'Microfilm'},
    {key: 'offsite', text: 'Offsite', value: 'Offsite'},
    {key: 'processing', text: 'Processing', value: 'Processing'},
    {key: 'not_found', text: 'Not Found', value: 'Not_Found'},
    {key: 'undeliverable', text: 'Undeliverable', value: 'Undeliverable'},
    {key: 'refund', text: 'Refund', value: 'Refund'},
    {key: 'done', text: 'Done', value: 'Done'}
];

export const deliveryMethodOptions = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'mail', text: 'Mail', value: 'mail'},
    {key: 'pickup', text: 'Pickup', value: 'pickup'},
    {key: 'email', text: 'Email', value: 'email'}
];