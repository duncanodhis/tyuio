/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  CForm,
  CFormInput,
  CFormFeedback,
  CCol,
  CButton,
  CContainer,
  CFormSelect,
  CInputGroup,
  CFormLabel,
} from '@coreui/react';

const AddPackage = () => {
  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState('');
  const [image, setImage] = useState(null);
  const [title, setTitle] = useState('');
  const [currency, setCurrency] = useState('');
  const [price, setPrice] = useState('');
  const [weight, setWeight] = useState('');
  const [quantity, setQuantity] = useState('');
  const [description, setDescription] = useState('');
  const [validated, setValidated] = useState(false);

  // Fetch categories from the server using useEffect
  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/categories');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();
  
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      setValidated(true);
    } else {
      try {
        const formData = new FormData();
        formData.append('category_name', newCategory);
        formData.append('image', image);
        formData.append('name', title);
        formData.append('currency', currency);
        formData.append('price', price);
        formData.append('weight', weight);
        formData.append('weight_measurement', quantity);
        formData.append('description', description); 
  
        const response = await axios.post('http://127.0.0.1:5000//api/packages', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        // Handle the response if needed
        console.log('Package created successfully:', response.data);
  
        // Reset the form and validation state
        setNewCategory('');
        setImage(null);
        setTitle('');
        setCurrency('');
        setPrice('');
        setWeight('');
        setQuantity('');
        setDescription(''); // Reset package description
        setValidated(false);
      } catch (error) {
        console.error('Error creating package:', error);
      }
    }
  };
  
  const handleCategoryChange = (event) => {
    setNewCategory(event.target.value);
  };

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleCurrencyChange = (event) => {
    setCurrency(event.target.value);
  };

  const handlePriceChange = (event) => {
    setPrice(event.target.value);
  };

  const handleWeightChange = (event) => {
    setWeight(event.target.value);
  };

  const handleQuantityChange = (event) => {
    setQuantity(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  return (
    <CContainer>
      <h2>Add Packaging</h2>
      <CForm className="row g-3 needs-validation" noValidate validated={validated} onSubmit={handleSubmit}>
        {/* Rest of the form code */}
        <CCol md={6}>
          <CFormSelect
            value={newCategory}
            onChange={handleCategoryChange}
            aria-label="Select Category"
            required
          >
            <option value="">Select a Category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.name}>
                {category.name}
              </option>
            ))}
          </CFormSelect>
          <CFormFeedback invalid>Please select a category.</CFormFeedback>
        </CCol>
        <CCol md={6}>
          <CFormInput type="file" onChange={handleImageChange} required />
          <CFormFeedback invalid>Please select an image.</CFormFeedback>
        </CCol>
        <CCol md={6}>
          <CFormInput
            type="text"
            value={title}
            onChange={handleTitleChange}
            placeholder="Enter title"
            required
          />
          <CFormFeedback invalid>Please enter a title.</CFormFeedback>
        </CCol>
        <CCol md={6}>
          <CInputGroup>
            <CFormSelect value={currency} onChange={handleCurrencyChange} required>
              <option value="">Select Currency</option>
              <option value="GEL">GEL</option>
              <option value="EUR">EUR</option>
            </CFormSelect>
            <CFormInput
              type="number"
              value={price}
              onChange={handlePriceChange}
              placeholder="Enter price"
              required
            />
            <CFormFeedback invalid>Please enter a valid price.</CFormFeedback>
          </CInputGroup>
        </CCol>
        <CCol md={6}>
          <CFormFeedback invalid>Please enter a valid weight.</CFormFeedback>
          <CInputGroup>
            <CFormSelect value={quantity} onChange={handleQuantityChange} required>
              <option value="">Select Quantity</option>
              <option value="grams">Grams</option>
              <option value="milligrams">Milligrams</option>
              <option value="pieces">Pieces</option>
            </CFormSelect>
            <CFormInput
              type="number"
              value={weight}
              onChange={handleWeightChange}
              placeholder="Enter weight"
              required
            />
            <CFormFeedback invalid>Please enter a valid weight.</CFormFeedback>
          </CInputGroup>
        </CCol>
        <CCol md={6}>
         
        </CCol>
        <CCol md={12}>
          <CFormLabel htmlFor="description">Package Description</CFormLabel>
          <CFormInput
            type="textarea"
            size="lg"
            id="description"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Enter package description"
            required
          />
          <CFormFeedback invalid>Please enter a package description.</CFormFeedback>
        </CCol>
        <CCol md={12}>
          <CButton color="primary" type="submit">
            Save package
          </CButton>
        </CCol>
      </CForm>
    </CContainer>
  );
};

export default AddPackage;

