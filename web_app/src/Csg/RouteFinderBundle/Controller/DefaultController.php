<?php

namespace Csg\RouteFinderBundle\Controller;

use Csg\RouteFinderBundle\Service\RecentSearch;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Csg\RouteFinderBundle\Service\RouteFinder;

/**
 * Class DefaultController
 * @package Csg\RouteFinderBundle\Command
 */
class DefaultController extends Controller
{
    /**
     * Main search view
     * 
     * @return \Symfony\Component\HttpFoundation\Response
     */
    public function indexAction()
    {
        /** @var $recentSearchService RecentSearch */
        $recentSearchService = $this->get('csg_route_finder.service.recent_search');
        $data = array();
        
        $queries = $this->getRequest()->query->all();
        $data['init_search'] = false;

        if (isset($queries['ft']) && isset($queries['fg']) && isset($queries['tt']) 
            && isset($queries['tg']) && isset($queries['t'])) {
            $data['from_latitude'] = (float) $queries['ft'];
            $data['from_longitude'] = (float) $queries['fg'];
            $data['to_latitude'] = (float) $queries['tt'];
            $data['to_longitude'] = (float) $queries['tg'];
            $data['time'] = new \DateTime('@' . (int) $queries['t']);

            $data['init_search'] = true;
        }

        $data['recent_search'] = $recentSearchService->getAll();
        
        foreach ($data['recent_search'] as $i => $recentSearchItem) {
            $urlData = array(
                'ft' => $recentSearchItem['from_coordinate_lat'],
                'fg' => $recentSearchItem['from_coordinate_long'],
                'tt' => $recentSearchItem['to_coordinate_lat'],
                'tg' => $recentSearchItem['to_coordinate_long'],
                't' => $recentSearchItem['start_time'],
            );
            
            $data['recent_search'][$i]['url'] = http_build_query($urlData);
        }
        
        return $this->render('CsgRouteFinderBundle:Default:index.html.twig', $data);
    }

    /**
     * Ajax searching function
     * 
     * @return Response
     */
    public function ajaxCalculateRouteAction()
    {
        
        /** @var $request Request */
        $request = $this->getRequest();
        /** @var $routeFinder RouteFinder */
        $routeFinder = $this->get('csg_route_finder.service.route_finder');


        $data = $request->request->all();
        $responseData = array();
        $responseData['error'] = true;

        if (empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
            || empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
            || empty($data['from_coordinate_lat'])) {
            return new JsonResponse($responseData);
        }

        $routes = $routeFinder->findRoutes(
            $data['from_coordinate_lat'],
            $data['from_coordinate_long'],
            $data['to_coordinate_lat'],
            $data['to_coordinate_long'],
            $data['start_time']
        );

        /** @var $recentSearchService RecentSearch */
        $recentSearchService = $this->get('csg_route_finder.service.recent_search');
        $recentSearchService->add($data);

//        $routes = $routeFinder->findRoutes(10, 20, 30, 40, 50);
        
        $responseData['error'] = false;
        
        $responseData['html'] = $this->renderView('CsgRouteFinderBundle:Finder:_results.html.twig', array(
            'routes' => $routes,
        ));
        
        return new JsonResponse($responseData);
    }
}
