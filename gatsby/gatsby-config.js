module.exports = {
  pathPrefix: `/`,
  siteMetadata: {
    title: 'kyle harrington\'s cold-storage album catalog',
    subtitle: 'cryoET solutions across tools and domains',
    catalog_url: 'http://cold-storage.kyleharrington.com',
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
