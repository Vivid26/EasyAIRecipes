import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

export const generateRecipe = async (ingredients) => {
  const res = await axios.post(`${BASE_URL}/generate`, { ingredients });
  return res.data;
};

export const saveRecipe = async (recipe) => {
  const res = await axios.post(`${BASE_URL}/save`, recipe);
  return res.data;
};

export const getFavorites = async () => {
  const res = await axios.get(`${BASE_URL}/favorites`);
  return res.data;
};
