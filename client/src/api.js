import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

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
