/* eslint-disable prettier/prettier */
/* eslint-disable react/prop-types */
import React, { useState, useEffect } from 'react';
import {
  CButton,
  CCollapse,
  CCard,
  CCardBody,
  CRow,
  CCol,
  CTable,
  CTableHead,
  CTableRow,
  CTableDataCell,
  CTableBody,
  CTableHeaderCell,
} from '@coreui/react';
import axios from 'axios';

const TaskModal = () => {
  const [visibleA, setVisibleA] = useState(false);
  const [selectedCourier, setSelectedCourier] = useState(null);
  const [selectedTask, setSelectedTask] = useState(null);
  const [couriers, setCouriers] = useState([]);

  useEffect(() => {
    // Fetch the couriers from the API
    const fetchCouriers = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/couriers_with_tasks');
        setCouriers(response.data);
      } catch (error) {
        console.error('Error fetching couriers:', error);
      }
    };

    fetchCouriers();
  }, []);

  // Sort the tasks based on the lastUpdated property (descending order) for each courier
  couriers.forEach(courier => {
    courier.tasks.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  });

  const handleViewTasks = (courier) => {
    setSelectedCourier(courier);
    setVisibleA(true);
  };

  const handleCollapseTask = (taskId) => {
    setSelectedTask(selectedTask === taskId ? null : taskId);
  };

  const formatLastUpdated = (dateTimeString) => {
    const options = { hour: 'numeric', minute: 'numeric', second: 'numeric' };
    return new Date(dateTimeString).toLocaleTimeString([], options);
  };

  return (
    <>
      {couriers.map((courier) => (
        <React.Fragment key={courier.id}>
          <CButton size="lg" onClick={() => handleViewTasks(courier)}>
            {courier.name}
          </CButton>
          {visibleA && selectedCourier && selectedCourier.id === courier.id && (
            <CRow>
              <CCol xs={6}>
                <CCollapse visible={visibleA}>
                  <CCard className="mt-3">
                    <CCardBody>
                      <CTable  hover>
                        <CTableHead>
                          <CTableRow>
                            <CTableHeaderCell scope="col">Task ID</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Status</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Treasures</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Last Updated</CTableHeaderCell>
                          </CTableRow>
                        </CTableHead>
                        <CTableBody>
                          {courier.tasks.map((task) => (
                            <React.Fragment key={`${courier.id}-${task.id}`}>
                              <CTableRow onClick={() => handleCollapseTask(task.id)}>
                                <CTableHeaderCell scope="row">{task.name}</CTableHeaderCell>
                                <CTableDataCell>{task.status}</CTableDataCell>
                                <CTableDataCell>{task.treasure}</CTableDataCell>
                                <CTableDataCell>{formatLastUpdated(task.updated_at)}</CTableDataCell>
                              </CTableRow>
                              <CCollapse visible={selectedTask === task.id}>
                                <CTableRow>
                                {selectedTask === task.id && (
                                  <CCollapse visible={selectedTask === task.id}>
                                    <CTableRow>
                                      <CTableDataCell colSpan="4" color="">
                                        <p>Task Details:</p>
                                        <p>Area of Distribution: {task.area_of_distribution}</p>
                                        <p>Commission: {task.commission}</p>
                                        <p>Commission Currency: {task.commission_currency}</p>
                                        <p>Cost of Item: {task.cost_of_item}</p>
                                        <p>Weight of Item: {task.weight_of_item}</p>
                                        {/* Add more task details here */}
                                        <p>Courier Details:</p>
                                        <p>Name: {selectedCourier.name}</p>
                                        <p>Password: {selectedCourier.password}</p>
                                        {/* Add more courier details here */}
                                      </CTableDataCell>
                                    </CTableRow>
                                  </CCollapse>
                            )}
                                </CTableRow>
                              </CCollapse>
                            </React.Fragment>
                          ))}
                        </CTableBody>
                      </CTable>
                    </CCardBody>
                  </CCard>
                </CCollapse>
              </CCol>
            </CRow>
          )}
        </React.Fragment>
      ))}
    </>
  );
};

export default TaskModal;
