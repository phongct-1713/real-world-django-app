/**
 * Conduit - Real World App Frontend
 * Single Page Application with hash-based routing
 */

// ===========================================
// Configuration & State
// ===========================================
const API_URL = '/api';
const DEFAULT_IMAGE = 'https://api.realworld.io/images/smiley-cyrus.jpg';

let state = {
  user: null,
  token: localStorage.getItem('token'),
  currentPage: 'home',
  articles: [],
  articlesCount: 0,
  tags: [],
  currentArticle: null,
  currentProfile: null,
  currentTab: 'global',
  currentTag: null,
  offset: 0,
  limit: 10
};

// ===========================================
// API Helper Functions
// ===========================================
async function api(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  if (state.token) {
    headers['Authorization'] = `Token ${state.token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (response.status === 204) {
    return null;
  }

  const data = await response.json();

  if (!response.ok) {
    throw data;
  }

  return data;
}

// ===========================================
// Auth Functions
// ===========================================
async function login(email, password) {
  const data = await api('/users/login/', {
    method: 'POST',
    body: JSON.stringify({ user: { email, password } })
  });
  state.token = data.user.token;
  state.user = data.user;
  localStorage.setItem('token', data.user.token);
  return data.user;
}

async function register(username, email, password) {
  const data = await api('/users/', {
    method: 'POST',
    body: JSON.stringify({ user: { username, email, password } })
  });
  state.token = data.user.token;
  state.user = data.user;
  localStorage.setItem('token', data.user.token);
  return data.user;
}

async function getCurrentUser() {
  if (!state.token) return null;
  try {
    const data = await api('/user/');
    state.user = data.user;
    return data.user;
  } catch (e) {
    logout();
    return null;
  }
}

async function updateUser(userData) {
  const data = await api('/user/', {
    method: 'PUT',
    body: JSON.stringify({ user: userData })
  });
  state.user = data.user;
  state.token = data.user.token;
  localStorage.setItem('token', data.user.token);
  return data.user;
}

function logout() {
  state.token = null;
  state.user = null;
  localStorage.removeItem('token');
  navigate('/');
}

// ===========================================
// Article Functions
// ===========================================
async function getArticles(params = {}) {
  const query = new URLSearchParams({
    limit: params.limit || state.limit,
    offset: params.offset || 0,
    ...params
  });
  delete query.delete('limit');
  delete query.delete('offset');
  
  let queryStr = `limit=${params.limit || state.limit}&offset=${params.offset || 0}`;
  if (params.tag) queryStr += `&tag=${params.tag}`;
  if (params.author) queryStr += `&author=${params.author}`;
  if (params.favorited) queryStr += `&favorited=${params.favorited}`;
  
  const data = await api(`/articles/?${queryStr}`);
  return data;
}

async function getFeed(params = {}) {
  const queryStr = `limit=${params.limit || state.limit}&offset=${params.offset || 0}`;
  const data = await api(`/articles/feed/?${queryStr}`);
  return data;
}

async function getArticle(slug) {
  const data = await api(`/articles/${slug}/`);
  return data.article;
}

async function createArticle(article) {
  const data = await api('/articles/', {
    method: 'POST',
    body: JSON.stringify({ article })
  });
  return data.article;
}

async function updateArticle(slug, article) {
  const data = await api(`/articles/${slug}/`, {
    method: 'PUT',
    body: JSON.stringify({ article })
  });
  return data.article;
}

async function deleteArticle(slug) {
  await api(`/articles/${slug}/`, { method: 'DELETE' });
}

async function favoriteArticle(slug) {
  const data = await api(`/articles/${slug}/favorite/`, { method: 'POST' });
  return data.article;
}

async function unfavoriteArticle(slug) {
  const data = await api(`/articles/${slug}/favorite/`, { method: 'DELETE' });
  return data.article;
}

// ===========================================
// Comment Functions
// ===========================================
async function getComments(slug) {
  const data = await api(`/articles/${slug}/comments/`);
  return data.comments;
}

async function addComment(slug, body) {
  const data = await api(`/articles/${slug}/comments/`, {
    method: 'POST',
    body: JSON.stringify({ comment: { body } })
  });
  return data.comment;
}

async function deleteComment(slug, commentId) {
  await api(`/articles/${slug}/comments/${commentId}/`, { method: 'DELETE' });
}

// ===========================================
// Profile Functions
// ===========================================
async function getProfile(username) {
  const data = await api(`/profiles/${username}/`);
  return data.profile;
}

async function followUser(username) {
  const data = await api(`/profiles/${username}/follow/`, { method: 'POST' });
  return data.profile;
}

async function unfollowUser(username) {
  const data = await api(`/profiles/${username}/follow/`, { method: 'DELETE' });
  return data.profile;
}

// ===========================================
// Tag Functions
// ===========================================
async function getTags() {
  const data = await api('/tags/');
  return data.tags;
}

// ===========================================
// Render Functions
// ===========================================
function renderNav() {
  const navLinks = document.getElementById('nav-links');
  const currentHash = window.location.hash || '#/';

  if (state.user) {
    navLinks.innerHTML = `
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/' ? 'active' : ''}" href="#/">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/editor' ? 'active' : ''}" href="#/editor">
          <i class="ion-compose"></i>&nbsp;New Article
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/settings' ? 'active' : ''}" href="#/settings">
          <i class="ion-gear-a"></i>&nbsp;Settings
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link ${currentHash.includes(`#/profile/${state.user.username}`) ? 'active' : ''}" href="#/profile/${state.user.username}">
          <img src="${state.user.image || DEFAULT_IMAGE}" class="user-pic" />
          ${state.user.username}
        </a>
      </li>
    `;
  } else {
    navLinks.innerHTML = `
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/' ? 'active' : ''}" href="#/">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/login' ? 'active' : ''}" href="#/login">Sign in</a>
      </li>
      <li class="nav-item">
        <a class="nav-link ${currentHash === '#/register' ? 'active' : ''}" href="#/register">Sign up</a>
      </li>
    `;
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

function renderArticlePreview(article) {
  return `
    <div class="article-preview">
      <div class="article-meta">
        <a href="#/profile/${article.author.username}">
          <img src="${article.author.image || DEFAULT_IMAGE}" />
        </a>
        <div class="info">
          <a href="#/profile/${article.author.username}" class="author">${article.author.username}</a>
          <span class="date">${formatDate(article.createdAt)}</span>
        </div>
        <button class="btn btn-outline-primary btn-sm pull-xs-right ${article.favorited ? 'active' : ''}" 
                onclick="handleFavorite('${article.slug}', ${article.favorited})">
          <i class="ion-heart"></i> ${article.favoritesCount}
        </button>
      </div>
      <a href="#/article/${article.slug}" class="preview-link">
        <h1>${article.title}</h1>
        <p>${article.description}</p>
        <span>Read more...</span>
        <ul class="tag-list">
          ${article.tagList.map(tag => `
            <li class="tag-default tag-pill tag-outline">${tag}</li>
          `).join('')}
        </ul>
      </a>
    </div>
  `;
}

function renderPagination(articlesCount, currentOffset) {
  const totalPages = Math.ceil(articlesCount / state.limit);
  if (totalPages <= 1) return '';
  
  let pages = '';
  for (let i = 0; i < totalPages; i++) {
    const offset = i * state.limit;
    pages += `
      <li class="page-item ${offset === currentOffset ? 'active' : ''}">
        <a class="page-link" href="javascript:void(0)" onclick="handlePageChange(${offset})">${i + 1}</a>
      </li>
    `;
  }
  
  return `<ul class="pagination">${pages}</ul>`;
}

// ===========================================
// Page Renderers
// ===========================================
async function renderHomePage() {
  const app = document.getElementById('app');
  
  // Load tags
  const tags = await getTags();
  
  app.innerHTML = `
    <div class="home-page">
      ${!state.user ? `
        <div class="banner">
          <div class="container">
            <h1 class="logo-font">conduit</h1>
            <p>A place to share your knowledge.</p>
          </div>
        </div>
      ` : ''}

      <div class="container page">
        <div class="row">
          <div class="col-md-9">
            <div class="feed-toggle">
              <ul class="nav nav-pills outline-active">
                ${state.user ? `
                  <li class="nav-item">
                    <a class="nav-link ${state.currentTab === 'feed' ? 'active' : ''}" 
                       href="javascript:void(0)" onclick="switchTab('feed')">Your Feed</a>
                  </li>
                ` : ''}
                <li class="nav-item">
                  <a class="nav-link ${state.currentTab === 'global' ? 'active' : ''}" 
                     href="javascript:void(0)" onclick="switchTab('global')">Global Feed</a>
                </li>
                ${state.currentTag ? `
                  <li class="nav-item">
                    <a class="nav-link active" href="javascript:void(0)">
                      <i class="ion-pound"></i> ${state.currentTag}
                    </a>
                  </li>
                ` : ''}
              </ul>
            </div>

            <div id="articles-container">
              <div class="article-preview">Loading articles...</div>
            </div>
            
            <div id="pagination-container"></div>
          </div>

          <div class="col-md-3">
            <div class="sidebar">
              <p>Popular Tags</p>
              <div class="tag-list">
                ${tags.map(tag => `
                  <a href="javascript:void(0)" class="tag-pill tag-default" onclick="filterByTag('${tag}')">${tag}</a>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  await loadArticles();
}

async function loadArticles() {
  const container = document.getElementById('articles-container');
  const paginationContainer = document.getElementById('pagination-container');
  
  try {
    let data;
    if (state.currentTab === 'feed') {
      data = await getFeed({ offset: state.offset, limit: state.limit });
    } else if (state.currentTag) {
      data = await getArticles({ tag: state.currentTag, offset: state.offset, limit: state.limit });
    } else {
      data = await getArticles({ offset: state.offset, limit: state.limit });
    }
    
    state.articles = data.articles;
    state.articlesCount = data.articlesCount;
    
    if (data.articles.length === 0) {
      container.innerHTML = '<div class="article-preview">No articles are here... yet.</div>';
    } else {
      container.innerHTML = data.articles.map(renderArticlePreview).join('');
    }
    
    paginationContainer.innerHTML = renderPagination(data.articlesCount, state.offset);
  } catch (e) {
    container.innerHTML = '<div class="article-preview">Error loading articles.</div>';
  }
}

async function renderLoginPage() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="auth-page">
      <div class="container page">
        <div class="row">
          <div class="col-md-6 offset-md-3 col-xs-12">
            <h1 class="text-xs-center">Sign in</h1>
            <p class="text-xs-center">
              <a href="#/register">Need an account?</a>
            </p>

            <ul class="error-messages" id="error-messages"></ul>

            <form id="login-form">
              <fieldset class="form-group">
                <input class="form-control form-control-lg" type="email" placeholder="Email" id="email" required />
              </fieldset>
              <fieldset class="form-group">
                <input class="form-control form-control-lg" type="password" placeholder="Password" id="password" required />
              </fieldset>
              <button class="btn btn-lg btn-primary pull-xs-right" type="submit">Sign in</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorList = document.getElementById('error-messages');
    
    try {
      await login(email, password);
      renderNav();
      navigate('/');
    } catch (err) {
      errorList.innerHTML = formatErrors(err.errors || { error: ['Invalid credentials'] });
    }
  });
}

async function renderRegisterPage() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="auth-page">
      <div class="container page">
        <div class="row">
          <div class="col-md-6 offset-md-3 col-xs-12">
            <h1 class="text-xs-center">Sign up</h1>
            <p class="text-xs-center">
              <a href="#/login">Have an account?</a>
            </p>

            <ul class="error-messages" id="error-messages"></ul>

            <form id="register-form">
              <fieldset class="form-group">
                <input class="form-control form-control-lg" type="text" placeholder="Username" id="username" required />
              </fieldset>
              <fieldset class="form-group">
                <input class="form-control form-control-lg" type="email" placeholder="Email" id="email" required />
              </fieldset>
              <fieldset class="form-group">
                <input class="form-control form-control-lg" type="password" placeholder="Password" id="password" required minlength="8" />
              </fieldset>
              <button class="btn btn-lg btn-primary pull-xs-right" type="submit">Sign up</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorList = document.getElementById('error-messages');
    
    try {
      await register(username, email, password);
      renderNav();
      navigate('/');
    } catch (err) {
      errorList.innerHTML = formatErrors(err.errors || { error: ['Registration failed'] });
    }
  });
}

async function renderSettingsPage() {
  if (!state.user) {
    navigate('/login');
    return;
  }

  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="settings-page">
      <div class="container page">
        <div class="row">
          <div class="col-md-6 offset-md-3 col-xs-12">
            <h1 class="text-xs-center">Your Settings</h1>

            <ul class="error-messages" id="error-messages"></ul>

            <form id="settings-form">
              <fieldset>
                <fieldset class="form-group">
                  <input class="form-control" type="text" placeholder="URL of profile picture" id="image" value="${state.user.image || ''}" />
                </fieldset>
                <fieldset class="form-group">
                  <input class="form-control form-control-lg" type="text" placeholder="Your Name" id="username" value="${state.user.username}" required />
                </fieldset>
                <fieldset class="form-group">
                  <textarea
                    class="form-control form-control-lg"
                    rows="8"
                    placeholder="Short bio about you"
                    id="bio"
                  >${state.user.bio || ''}</textarea>
                </fieldset>
                <fieldset class="form-group">
                  <input class="form-control form-control-lg" type="email" placeholder="Email" id="email" value="${state.user.email}" required />
                </fieldset>
                <fieldset class="form-group">
                  <input
                    class="form-control form-control-lg"
                    type="password"
                    placeholder="New Password"
                    id="password"
                  />
                </fieldset>
                <button class="btn btn-lg btn-primary pull-xs-right" type="submit">Update Settings</button>
              </fieldset>
            </form>
            <hr />
            <button class="btn btn-outline-danger" onclick="handleLogout()">Or click here to logout.</button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('settings-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorList = document.getElementById('error-messages');
    
    const userData = {
      image: document.getElementById('image').value,
      username: document.getElementById('username').value,
      bio: document.getElementById('bio').value,
      email: document.getElementById('email').value
    };
    
    const password = document.getElementById('password').value;
    if (password) {
      userData.password = password;
    }
    
    try {
      await updateUser(userData);
      renderNav();
      navigate(`/profile/${state.user.username}`);
    } catch (err) {
      errorList.innerHTML = formatErrors(err.errors || { error: ['Update failed'] });
    }
  });
}

async function renderEditorPage(slug = null) {
  if (!state.user) {
    navigate('/login');
    return;
  }

  let article = { title: '', description: '', body: '', tagList: [] };
  
  if (slug) {
    try {
      article = await getArticle(slug);
    } catch (e) {
      navigate('/');
      return;
    }
  }

  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="editor-page">
      <div class="container page">
        <div class="row">
          <div class="col-md-10 offset-md-1 col-xs-12">
            <ul class="error-messages" id="error-messages"></ul>

            <form id="editor-form">
              <fieldset>
                <fieldset class="form-group">
                  <input type="text" class="form-control form-control-lg" placeholder="Article Title" id="title" value="${article.title}" required />
                </fieldset>
                <fieldset class="form-group">
                  <input type="text" class="form-control" placeholder="What's this article about?" id="description" value="${article.description}" required />
                </fieldset>
                <fieldset class="form-group">
                  <textarea
                    class="form-control"
                    rows="8"
                    placeholder="Write your article (in markdown)"
                    id="body"
                    required
                  >${article.body}</textarea>
                </fieldset>
                <fieldset class="form-group">
                  <input type="text" class="form-control" placeholder="Enter tags (comma separated)" id="tags" value="${article.tagList.join(', ')}" />
                </fieldset>
                <button class="btn btn-lg pull-xs-right btn-primary" type="submit">
                  Publish Article
                </button>
              </fieldset>
            </form>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('editor-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorList = document.getElementById('error-messages');
    
    const articleData = {
      title: document.getElementById('title').value,
      description: document.getElementById('description').value,
      body: document.getElementById('body').value,
      tagList: document.getElementById('tags').value.split(',').map(t => t.trim()).filter(t => t)
    };
    
    try {
      let result;
      if (slug) {
        result = await updateArticle(slug, articleData);
      } else {
        result = await createArticle(articleData);
      }
      navigate(`/article/${result.slug}`);
    } catch (err) {
      errorList.innerHTML = formatErrors(err.errors || { error: ['Failed to publish'] });
    }
  });
}

async function renderArticlePage(slug) {
  const app = document.getElementById('app');
  
  try {
    const article = await getArticle(slug);
    const comments = await getComments(slug);
    state.currentArticle = article;
    
    const isAuthor = state.user && state.user.username === article.author.username;
    
    app.innerHTML = `
      <div class="article-page">
        <div class="banner">
          <div class="container">
            <h1>${article.title}</h1>

            <div class="article-meta">
              <a href="#/profile/${article.author.username}">
                <img src="${article.author.image || DEFAULT_IMAGE}" />
              </a>
              <div class="info">
                <a href="#/profile/${article.author.username}" class="author">${article.author.username}</a>
                <span class="date">${formatDate(article.createdAt)}</span>
              </div>
              ${isAuthor ? `
                <a class="btn btn-sm btn-outline-secondary" href="#/editor/${article.slug}">
                  <i class="ion-edit"></i> Edit Article
                </a>
                <button class="btn btn-sm btn-outline-danger" onclick="handleDeleteArticle('${article.slug}')">
                  <i class="ion-trash-a"></i> Delete Article
                </button>
              ` : `
                <button class="btn btn-sm btn-outline-secondary" onclick="handleFollow('${article.author.username}', ${article.author.following})">
                  <i class="ion-plus-round"></i>
                  &nbsp; ${article.author.following ? 'Unfollow' : 'Follow'} ${article.author.username}
                </button>
                &nbsp;&nbsp;
                <button class="btn btn-sm ${article.favorited ? 'btn-primary' : 'btn-outline-primary'}" onclick="handleFavoriteArticle('${article.slug}', ${article.favorited})">
                  <i class="ion-heart"></i>
                  &nbsp; ${article.favorited ? 'Unfavorite' : 'Favorite'} Article <span class="counter">(${article.favoritesCount})</span>
                </button>
              `}
            </div>
          </div>
        </div>

        <div class="container page">
          <div class="row article-content">
            <div class="col-md-12">
              <div id="article-body">${marked.parse(article.body)}</div>
              <ul class="tag-list">
                ${article.tagList.map(tag => `
                  <li class="tag-default tag-pill tag-outline">${tag}</li>
                `).join('')}
              </ul>
            </div>
          </div>

          <hr />

          <div class="row">
            <div class="col-xs-12 col-md-8 offset-md-2">
              ${state.user ? `
                <form class="card comment-form" id="comment-form">
                  <div class="card-block">
                    <textarea class="form-control" placeholder="Write a comment..." rows="3" id="comment-body" required></textarea>
                  </div>
                  <div class="card-footer">
                    <img src="${state.user.image || DEFAULT_IMAGE}" class="comment-author-img" />
                    <button class="btn btn-sm btn-primary" type="submit">Post Comment</button>
                  </div>
                </form>
              ` : `
                <p>
                  <a href="#/login">Sign in</a> or <a href="#/register">sign up</a> to add comments on this article.
                </p>
              `}

              <div id="comments-container">
                ${comments.map(comment => renderComment(comment, article.slug)).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    
    if (state.user) {
      document.getElementById('comment-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const body = document.getElementById('comment-body').value;
        try {
          const comment = await addComment(slug, body);
          document.getElementById('comment-body').value = '';
          const container = document.getElementById('comments-container');
          container.innerHTML = renderComment(comment, slug) + container.innerHTML;
        } catch (err) {
          alert('Failed to post comment');
        }
      });
    }
  } catch (e) {
    app.innerHTML = '<div class="container"><p>Article not found.</p></div>';
  }
}

function renderComment(comment, slug) {
  const canDelete = state.user && state.user.username === comment.author.username;
  return `
    <div class="card" id="comment-${comment.id}">
      <div class="card-block">
        <p class="card-text">${comment.body}</p>
      </div>
      <div class="card-footer">
        <a href="#/profile/${comment.author.username}" class="comment-author">
          <img src="${comment.author.image || DEFAULT_IMAGE}" class="comment-author-img" />
        </a>
        &nbsp;
        <a href="#/profile/${comment.author.username}" class="comment-author">${comment.author.username}</a>
        <span class="date-posted">${formatDate(comment.createdAt)}</span>
        ${canDelete ? `
          <span class="mod-options">
            <i class="ion-trash-a" onclick="handleDeleteComment('${slug}', ${comment.id})" style="cursor: pointer;"></i>
          </span>
        ` : ''}
      </div>
    </div>
  `;
}

async function renderProfilePage(username, tab = 'my') {
  const app = document.getElementById('app');
  
  try {
    const profile = await getProfile(username);
    state.currentProfile = profile;
    
    const isCurrentUser = state.user && state.user.username === username;
    
    app.innerHTML = `
      <div class="profile-page">
        <div class="user-info">
          <div class="container">
            <div class="row">
              <div class="col-xs-12 col-md-10 offset-md-1">
                <img src="${profile.image || DEFAULT_IMAGE}" class="user-img" />
                <h4>${profile.username}</h4>
                <p>${profile.bio || ''}</p>
                ${isCurrentUser ? `
                  <a class="btn btn-sm btn-outline-secondary action-btn" href="#/settings">
                    <i class="ion-gear-a"></i>
                    &nbsp; Edit Profile Settings
                  </a>
                ` : `
                  <button class="btn btn-sm ${profile.following ? 'btn-secondary' : 'btn-outline-secondary'} action-btn" onclick="handleFollowProfile('${profile.username}', ${profile.following})">
                    <i class="ion-plus-round"></i>
                    &nbsp; ${profile.following ? 'Unfollow' : 'Follow'} ${profile.username}
                  </button>
                `}
              </div>
            </div>
          </div>
        </div>

        <div class="container">
          <div class="row">
            <div class="col-xs-12 col-md-10 offset-md-1">
              <div class="articles-toggle">
                <ul class="nav nav-pills outline-active">
                  <li class="nav-item">
                    <a class="nav-link ${tab === 'my' ? 'active' : ''}" href="#/profile/${username}">My Articles</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link ${tab === 'favorites' ? 'active' : ''}" href="#/profile/${username}/favorites">Favorited Articles</a>
                  </li>
                </ul>
              </div>

              <div id="profile-articles">
                <div class="article-preview">Loading articles...</div>
              </div>
              
              <div id="profile-pagination"></div>
            </div>
          </div>
        </div>
      </div>
    `;
    
    await loadProfileArticles(username, tab);
  } catch (e) {
    app.innerHTML = '<div class="container"><p>Profile not found.</p></div>';
  }
}

async function loadProfileArticles(username, tab) {
  const container = document.getElementById('profile-articles');
  const paginationContainer = document.getElementById('profile-pagination');
  
  try {
    let data;
    if (tab === 'favorites') {
      data = await getArticles({ favorited: username, offset: state.offset, limit: state.limit });
    } else {
      data = await getArticles({ author: username, offset: state.offset, limit: state.limit });
    }
    
    if (data.articles.length === 0) {
      container.innerHTML = '<div class="article-preview">No articles are here... yet.</div>';
    } else {
      container.innerHTML = data.articles.map(renderArticlePreview).join('');
    }
    
    paginationContainer.innerHTML = renderPagination(data.articlesCount, state.offset);
  } catch (e) {
    container.innerHTML = '<div class="article-preview">Error loading articles.</div>';
  }
}

// ===========================================
// Event Handlers
// ===========================================
function handleLogout() {
  logout();
  renderNav();
}

async function handleFavorite(slug, isFavorited) {
  if (!state.user) {
    navigate('/login');
    return;
  }
  
  try {
    if (isFavorited) {
      await unfavoriteArticle(slug);
    } else {
      await favoriteArticle(slug);
    }
    await loadArticles();
  } catch (e) {
    console.error('Failed to favorite article');
  }
}

async function handleFavoriteArticle(slug, isFavorited) {
  if (!state.user) {
    navigate('/login');
    return;
  }
  
  try {
    if (isFavorited) {
      await unfavoriteArticle(slug);
    } else {
      await favoriteArticle(slug);
    }
    await renderArticlePage(slug);
  } catch (e) {
    console.error('Failed to favorite article');
  }
}

async function handleFollow(username, isFollowing) {
  if (!state.user) {
    navigate('/login');
    return;
  }
  
  try {
    if (isFollowing) {
      await unfollowUser(username);
    } else {
      await followUser(username);
    }
    await renderArticlePage(state.currentArticle.slug);
  } catch (e) {
    console.error('Failed to follow user');
  }
}

async function handleFollowProfile(username, isFollowing) {
  if (!state.user) {
    navigate('/login');
    return;
  }
  
  try {
    if (isFollowing) {
      await unfollowUser(username);
    } else {
      await followUser(username);
    }
    await renderProfilePage(username);
  } catch (e) {
    console.error('Failed to follow user');
  }
}

async function handleDeleteArticle(slug) {
  if (confirm('Are you sure you want to delete this article?')) {
    try {
      await deleteArticle(slug);
      navigate('/');
    } catch (e) {
      alert('Failed to delete article');
    }
  }
}

async function handleDeleteComment(slug, commentId) {
  if (confirm('Are you sure you want to delete this comment?')) {
    try {
      await deleteComment(slug, commentId);
      document.getElementById(`comment-${commentId}`).remove();
    } catch (e) {
      alert('Failed to delete comment');
    }
  }
}

function switchTab(tab) {
  state.currentTab = tab;
  state.currentTag = null;
  state.offset = 0;
  renderHomePage();
}

function filterByTag(tag) {
  state.currentTab = 'tag';
  state.currentTag = tag;
  state.offset = 0;
  renderHomePage();
}

function handlePageChange(offset) {
  state.offset = offset;
  loadArticles();
  window.scrollTo(0, 0);
}

function formatErrors(errors) {
  let html = '';
  for (const [key, messages] of Object.entries(errors)) {
    for (const message of messages) {
      html += `<li>${key} ${message}</li>`;
    }
  }
  return html;
}

// ===========================================
// Router
// ===========================================
function navigate(path) {
  window.location.hash = '#' + path;
}

async function router() {
  const hash = window.location.hash || '#/';
  const path = hash.slice(1); // Remove the #
  
  state.offset = 0;
  
  // Parse route
  if (path === '/' || path === '') {
    await renderHomePage();
  } else if (path === '/login') {
    await renderLoginPage();
  } else if (path === '/register') {
    await renderRegisterPage();
  } else if (path === '/settings') {
    await renderSettingsPage();
  } else if (path === '/editor') {
    await renderEditorPage();
  } else if (path.startsWith('/editor/')) {
    const slug = path.replace('/editor/', '');
    await renderEditorPage(slug);
  } else if (path.startsWith('/article/')) {
    const slug = path.replace('/article/', '');
    await renderArticlePage(slug);
  } else if (path.startsWith('/profile/')) {
    const parts = path.replace('/profile/', '').split('/');
    const username = parts[0];
    const tab = parts[1] === 'favorites' ? 'favorites' : 'my';
    await renderProfilePage(username, tab);
  } else {
    await renderHomePage();
  }
  
  renderNav();
}

// ===========================================
// Initialize
// ===========================================
async function init() {
  // Try to get current user if token exists
  if (state.token) {
    await getCurrentUser();
  }
  
  // Set up hash change listener
  window.addEventListener('hashchange', router);
  
  // Initial render
  renderNav();
  await router();
}

// Start the app
init();
