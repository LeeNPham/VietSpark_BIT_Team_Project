import adapter from '@sveltejs/adapter-vercel';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {


	kit: {
		adapter: adapter(),
		alias: {
			$lib: path.resolve('./src/lib'),
			$models: path.resolve('./src/models'),
			$src: path.resolve('./src')
		}
	},

	preprocess: [],
	extensions: ['.svelte', '.svx']
};

export default config;
