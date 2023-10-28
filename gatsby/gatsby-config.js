module.exports = {
  pathPrefix: `/`,
  siteMetadata: {
    title: 'kyle harrington\'s cold-storage album for cryoET',
    subtitle: 'album solutions for processing/viz/ML of cryoET data',
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
