module.exports = {
  pathPrefix: `/test-catalog`,
  siteMetadata: {
    title: 'album catalog',
    subtitle: 'sharing favourite solutions across tools and domains',
    catalog_url: 'https://github.com/frauzufall/test-catalog',
    menuLinks:[
      {
         name:'Catalog',
         link:'/catalog'
      },
      {
         name:'About',
         link:'/about'
      },
    ]
  },
  plugins: [{ resolve: `gatsby-theme-album`, options: {} }],
}
