import play.api.mvc.EssentialFilter;
import play.filters.cors.CORSFilter;
import play.http.HttpFilters;

import java.util.ArrayList;
import java.util.List;

import javax.inject.Inject;

public class Filters implements HttpFilters {

    @Inject
    CORSFilter corsFilter;

//    public EssentialFilter[] filters() {
//        return new EssentialFilter[] { corsFilter.asJava()  };
//    }

	@Override
	public List<play.mvc.EssentialFilter> getFilters() {
		// TODO Auto-generated method stub
		List<play.mvc.EssentialFilter> esf =  new ArrayList<play.mvc.EssentialFilter>();
	    esf.add(corsFilter.asJava());
	    return esf;
		//return null;
	}
}