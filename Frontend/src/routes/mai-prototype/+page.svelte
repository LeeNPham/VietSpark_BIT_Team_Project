<!-- <script>
	let tasks = [];
	let task = '';
	let alert = '';
	let alertType = '';
	let alertMessage = '';
	let alertColor = '';

	function addTask() {
		if (task === '') {
			alert = 'block';
			alertType = 'alert';
			alertMessage = 'Please enter a task.';
			alertColor = 'red';
			return;
		}
		tasks = [...tasks, { task }];
		task = '';
		alert = 'block';
		alertType = 'success';
		alertMessage = 'Task added!';
		alertColor = 'green';
	}
</script> -->

<div>
	<h1>Welcome to Mai's Tracker! 🧚‍♀️</h1>
	<br />
	<h2>About the Engineer</h2>
	<p>
		🌱 Hi, my name is Mai (they/them). I’m a software engineer/returning graduate at Techtonica with
		a passion for creating accessible features for people with disabilities.
		<br /><br />
		As someone who has a disability (i.e. being recently diagnosed with ADHD), I have a difficult time
		focusing on tasks without constant visual reminders.
		<br /><br />
		So, in a few weeks, you (the user) will be able to see a task tracker that also allows you to set
		reminders with alerts sent to your email or phone.
	</p>
	<br />
	<p class="w-full flex justify-center">
		<button> Here is a button </button>
	</p>

<!--
	<h3>Tracker</h3>

	<div>
		<input type="text" bind:value={task} placeholder="Add a task" />
		<button onclick={addTask}> Add Task </button>
	</div>

	<ul>
		{#each tasks as { task }}
			<li>{task}</li>
		{/each}
	</ul>
	<br /> -->

	<p>
		The engineer's current favorite song is "Hysteric" by Yeah Yeah Yeahs. 🎶
		<br /> <br />
		<iframe
			title="Music Player playing Hysteric by Yeah Yeah Yeahs"
			width="100%"
			height="166"
			scrolling="no"
			frameborder="no"
			src="https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/yeah-yeah-yeahs-official/hysteric-acoustic-1&color=ff5500"
		>
		</iframe>
	</p>
</div>

<style>

</style>
