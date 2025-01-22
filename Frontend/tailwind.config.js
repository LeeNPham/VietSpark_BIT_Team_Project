import containerQueries from '@tailwindcss/container-queries';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],
	darkMode: 'class',

	theme: {
		extend: {
			colors: {
				// flowbite-svelte
				//Customized Color Template
				primary: {
					50: '#E3F2FD', // Lightest blue
					100: '#BBDEFB',
					200: '#90CAF9',
					300: '#64B5F6',
					400: '#42A5F5',
					500: '#2196F3', // Main blue
					600: '#1E88E5',
					700: '#1976D2',
					800: '#1565C0',
					900: '#0D47A1',  // Darkest blue
					950:'#E7F2AC', // green
					1000: '#CCE5E3',// blue
				},
				background: {
					'white': '#F3F5F7',
				}
			}
		}
	},

	plugins: [typography, forms, containerQueries]
};
