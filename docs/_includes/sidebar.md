			<nav id="sidebar">
				<div class="p-4 pt-5">
		  		<a href="{{ '/' | relative_url }}">
          <img src="{{'images/logo/sphenix-logo-custom-bg.png' | relative_url}}" width="180"/>
          </a>
	        <ul class="list-unstyled components mb-5">
            <li>
              <a href="{{ '/' | relative_url }}">Home</a>
            </li>
            <li>
              <a href="{{ '/content/test_beam.html' | relative_url }}">Test Beam Data</a>
            </li>
            <li><!--  class="active" -->

	            <a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Software</a>
	            <ul class="collapse list-unstyled" id="homeSubmenu">
                <li>
                    <a href="{{ '/content/templates.html' | relative_url }}">Signal Templates</a>
                </li>

                <li>
                    <a href="{{ '/content/ml.html' | relative_url }}">ML techniques</a>
                </li>


                <li>
                    <a href="{{ '/content/docker.html' | relative_url }}">Docker</a>
                </li>
	            </ul>
	          </li>

	          <li>
              <a href="{{ '/content/contact.html' | relative_url }}">Contact</a>
	          </li>

            <li>
              <a href="{{ '/content/about.html' | relative_url }}">About this site</a>
          </li>
	        </ul>
      

          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>
          <ul>&nbsp;</ul>

	        <div class="footer">
	        	<p><!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
						  &copy;<script>document.write(new Date().getFullYear());</script> Bootstrap template by <a href="https://colorlib.com" target="_blank">Colorlib.com</a>
						  <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. --></p>
              <p>Site built<br/>  {{ site.time }}</p>
	        </div>

	      </div>
    	</nav>

        <!-- Page Content  -->
      <div id="content" class="p-4 p-md-5">

        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <div class="container-fluid">

            <button type="button" id="sidebarCollapse" class="btn btn-primary">
              <i class="fa fa-bars"></i>
              <span class="sr-only">Toggle Menu</span>
            </button>
            <button class="btn btn-dark d-inline-block d-lg-none ml-auto" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <i class="fa fa-bars"></i>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="nav navbar-nav ml-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="{{ '/' | relative_url }}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ '/content/contact.html' | relative_url }}">Contact</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="https://github.com/sPHENIX-Collaboration/calorimeter-signal-extraction" target="_blank"><img src="{{ 'images/logo/github_64.png' | relative_url }}" height="16" ></a>
              </li>
              </ul>
            </div>
          </div>
        </nav>