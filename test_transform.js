// Test frontend data transformation
const formData = {
  name: 'Test Business',
  type_of_provider: ['Tour Operator'],
  gstin: '',
  years: '5',
  website: '',
  reg_number: '',
  address: '123 Test Street',
  employees: '10',
  seasonal: false,
  annual_bookings: ''
};

// Transform data like the frontend does
const submitData = {
  ...formData,
  years: parseInt(formData.years),
  employees: parseInt(formData.employees),
  annual_bookings: formData.annual_bookings ? parseInt(formData.annual_bookings) : null,
  website: formData.website.trim() || null,
  gstin: formData.gstin.trim() || null,
  reg_number: formData.reg_number.trim() || null
};

console.log('Original data:', formData);
console.log('Transformed data:', submitData);
