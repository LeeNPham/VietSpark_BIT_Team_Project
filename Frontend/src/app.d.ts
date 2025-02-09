// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	// Define custom elements to prevent TypeScript errors
	interface HTMLElementTagNameMap {
		'nav-bar': HTMLElement;
		'nav-home': HTMLElement;
		'category-btn': HTMLElement;
		'category': HTMLElement;
	}
}

export {};
