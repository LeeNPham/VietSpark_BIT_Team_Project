<script>
	let name = "Tam"
	import { Footer, FooterCopyright, FooterLinkGroup, FooterLink, FooterBrand, FooterIcon } from 'flowbite-svelte';
	import { FacebookSolid, GithubSolid, DiscordSolid, TwitterSolid } from 'flowbite-svelte-icons';
</script>
<div class="bg-red-300 text-xl p-5 px-10 rounded-xl border-2 border-blue-500">
	Hello, my name is {name}

</div>

<div>
	Tam!!!!
	<br />
	This is going to be your prototype page~
	<br />
	Feel free to write down notes for yourself as well as what your primary goals are going to be, I would
	like for this to be a way of showcasing how you thoughtfully approached your prototype.
</div>
  
  <Footer footerType="socialmedia" class="bg-red-100">
	<div class="md:flex md:justify-between">
	  <div class="grid grid-cols-2 gap-8 sm:gap-6 sm:grid-cols-3">
		<div>
		  <h2 class="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Resources</h2>
		  <FooterLinkGroup>
			<FooterLink liClass="mb-4" href="/">Flowbite</FooterLink>
			<FooterLink liClass="mb-4" href="/">Tailwind CSS</FooterLink>
		  </FooterLinkGroup>
		</div>
		<div>
		  <h2 class="mb-6 text-sm font-semibold uppercase text-gray-900 dark:text-white">Follow us</h2>
		  <FooterLinkGroup>
			<FooterLink liClass="mb-4" href="/">GitHub</FooterLink>
			<FooterLink liClass="mb-4" href="/">Discord</FooterLink>
		  </FooterLinkGroup>
		</div>
		<div>
		  <h2 class="mb-6 text-sm font-semibold uppercase text-gray-900 dark:text-white">Legal</h2>
		  <FooterLinkGroup>
			<FooterLink liClass="mb-4" href="/">Privacy Policy</FooterLink>
			<FooterLink liClass="mb-4" href="/">Terms & Conditions</FooterLink>
		  </FooterLinkGroup>
		</div>
	  </div>
	</div>
	<hr class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
	<div class="sm:flex sm:items-center sm:justify-between">
	  <FooterCopyright href="/" by="Flowbite™" />
	  <div class="flex mt-4 space-x-6 rtl:space-x-reverse sm:justify-center sm:mt-0">
		<FooterIcon href="/">
		  <FacebookSolid class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white" />
		</FooterIcon>
		<FooterIcon href="/">
		  <DiscordSolid class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white" />
		</FooterIcon>
		<FooterIcon href="/">
		  <TwitterSolid class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white" />
		</FooterIcon>
		<FooterIcon href="/">
		  <GithubSolid class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white" />
		</FooterIcon>
		<FooterIcon href="/">
			hello word
		</FooterIcon>
	  </div>
	</div>
  </Footer>